"""Persistent memory implementation for LangChain using Alchemyst AI."""

import time
from typing import Any, Dict, List

from alchemyst_ai import AlchemystAI
from langchain_core.chat_history import BaseChatMessageHistory as BaseChatMemory


class AlchemystMemory(BaseChatMemory):
    """Persistent chat memory using Alchemyst AI..."""

    def __init__(
        self, api_key: str, session_id: str, org_id: str = "default", **kwargs: Any
    ) -> None:
        """Initialize AlchemystMemory.

        Args:
            api_key: Alchemyst AI API key
            session_id: Unique session identifier
            org_id: Alchemyst Organization ID
            **kwargs: Additional arguments for BaseChatMemory
        """
        self._session_id = session_id
        self._org_id = org_id
        self._client = AlchemystAI(api_key=api_key)

        # This call is safe because org_id is now an explicit argument
        # and is no longer hidden inside **kwargs
        super().__init__(**kwargs)

    @property
    def memory_variables(self) -> List[str]:
        """Return the list of memory variables.

        Returns:
            List containing ["history"]
        """
        return ["history"]

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Load conversation history from Alchemyst memory.

        Retrieves relevant conversation context from Alchemyst's memory service
        based on the current input. Uses semantic search to find the most
        relevant past messages for this session.

        Args:
            inputs: Dictionary containing the current input. Expected to have
                   an "input" key with the user's message.

        Returns:
            Dictionary with "history" key containing the conversation history
            as a newline-separated string of past messages.

        """
        try:
            # Use the input as query if available, otherwise use "conversation"
            query = (
                inputs.get("input", "").strip()
                if inputs.get("input")
                else "conversation"
            )

            # Search for relevant context in this session
            response = self._client.v1.context.search(
                query=query,
                similarity_threshold=0.0,
                minimum_similarity_threshold=0.0,
                scope="internal",
                body_metadata={"file_type": "text", "group_name": [self._session_id]},
            )

            # Extract context content
            contexts = response.contexts if response.contexts is not None else []
            items = [c.content for c in contexts if hasattr(c, "content") and c.content]

            return {"history": "\n".join(items)}

        except Exception as error:
            print(f"Error loading memory variables: {error}")
            return {"history": ""}

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, Any]) -> None:
        """Save conversation context to Alchemyst memory.

        Stores both the user input and AI output in Alchemyst's persistent
        memory, associated with this session ID.

        Args:
            inputs: Dictionary containing user input with "input" key
            outputs: Dictionary containing AI output with "output" key

        Example:
            >>> memory = AlchemystMemory(api_key="...", session_id="session-1")
            >>> memory.save_context(
            ...     inputs={"input": "What's the weather?"},
            ...     outputs={"output": "It's sunny today!"}
            ... )
        """
        user_input = str(inputs.get("input", ""))
        ai_output = str(outputs.get("output", ""))

        contents: List[Dict[str, Any]] = []
        timestamp = int(time.time() * 1000)  # milliseconds

        # Add user message
        if user_input:
            contents.append(
                {
                    "content": user_input,
                    "metadata": {
                        "source": self._session_id,
                        "messageId": str(timestamp),
                        "type": "text",
                    },
                }
            )

        # Add AI response
        if ai_output:
            contents.append(
                {
                    "content": ai_output,
                    "metadata": {
                        "source": self._session_id,
                        "messageId": str(timestamp + 1),
                        "type": "text",
                    },
                }
            )

        if not contents:
            return

        try:
            # Save to Alchemyst memory with session grouping
            self._client.v1.context.memory.add(
                session_id=self._session_id,
                contents=contents,
                metadata={
                    "group_name": [self._session_id],
                },
            )
        except Exception as error:
            print(f"Error saving context: {error}")

    def clear(self) -> None:
        """Clear all memory for this session.

        Deletes all stored conversation history associated with this session_id
        from Alchemyst's memory service.

        Example:
            >>> memory = AlchemystMemory(api_key="...", session_id="session-1")
            >>> memory.clear()  # All history for this session is deleted
        """
        try:
            self._client.v1.context.memory.delete(
                memory_id=self._session_id, organization_id="default"
            )
        except Exception as error:
            print(f"Error clearing memory: {error}")

    @property
    def memory_keys(self) -> List[str]:
        """Return the memory keys.

        Returns:
            List containing ["history"]
        """
        return ["history"]
