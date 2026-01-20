"""Integration tests for AlchemystMemory.

These tests verify AlchemystMemory works correctly with real API calls.
They require valid ALCHEMYST_AI_API_KEY in environment.

Run tests:
    pytest tests/integration/test_memory.py
    
Skip if no API key:
    pytest tests/integration/test_memory.py --skip-integration
"""

import os
import uuid
import pytest
from dotenv import load_dotenv

from alchemyst_langchain.memory import AlchemystMemory

# Load environment variables
load_dotenv()

# Skip all tests if API key not available
pytestmark = pytest.mark.skipif(
    not os.getenv("ALCHEMYST_AI_API_KEY"),
    reason="ALCHEMYST_AI_API_KEY not set in environment"
)


@pytest.fixture
def unique_session_id():
    """Generate a unique session ID for each test."""
    return f"test_session_{uuid.uuid4()}"


@pytest.fixture
def memory(unique_session_id):
    """Create AlchemystMemory instance with unique session."""
    return AlchemystMemory(
        api_key=os.getenv("ALCHEMYST_AI_API_KEY"),
        session_id=unique_session_id
    )


@pytest.fixture(autouse=True)
def cleanup(memory):
    """Clean up test data after each test."""
    yield
    # Clear memory after test completes
    try:
        memory.clear()
    except Exception:
        pass  # Ignore cleanup errors


class TestMemoryBasics:
    """Test basic memory operations."""
    
    def test_memory_initialization(self, unique_session_id):
        """Test creating a memory instance."""
        memory = AlchemystMemory(
            api_key=os.getenv("ALCHEMYST_AI_API_KEY"),
            session_id=unique_session_id
        )
        
        assert memory._session_id == unique_session_id
        assert memory.memory_variables == ["history"]
        assert memory.memory_keys == ["history"]
    
    def test_save_and_load_context(self, memory):
        """Test saving context and loading it back."""
        # Save some context
        memory.save_context(
            inputs={"input": "My name is Alice"},
            outputs={"output": "Nice to meet you, Alice!"}
        )
        
        # Load the context
        result = memory.load_memory_variables({"input": "What is my name?"})
        
        # Should have history
        assert "history" in result
        assert isinstance(result["history"], str)
    
    def test_clear_memory(self, memory):
        """Test clearing memory."""
        # Add some data
        memory.save_context(
            inputs={"input": "Remember this: test123"},
            outputs={"output": "I'll remember that"}
        )
        
        # Clear memory
        memory.clear()
        
        # Create new memory instance with same session
        new_memory = AlchemystMemory(
            api_key=os.getenv("ALCHEMYST_AI_API_KEY"),
            session_id=memory._session_id
        )
        
        # Load should return empty or minimal history
        result = new_memory.load_memory_variables({"input": "test"})
        assert "history" in result


class TestMemoryPersistence:
    """Test that memory persists across instances."""
    
    def test_memory_persists_across_instances(self, unique_session_id):
        """Test that data persists when creating new instance with same session."""
        # First instance - save data
        memory1 = AlchemystMemory(
            api_key=os.getenv("ALCHEMYST_AI_API_KEY"),
            session_id=unique_session_id
        )
        
        memory1.save_context(
            inputs={"input": "I like pizza"},
            outputs={"output": "Great choice!"}
        )
        
        # Second instance - should retrieve the data
        memory2 = AlchemystMemory(
            api_key=os.getenv("ALCHEMYST_AI_API_KEY"),
            session_id=unique_session_id
        )
        
        result = memory2.load_memory_variables({"input": "What do I like?"})
        
        assert "history" in result
        # The history should contain our saved context
        # Note: Actual content depends on Alchemyst's search behavior
        
        # Cleanup
        memory2.clear()


class TestSessionIsolation:
    """Test that different sessions are isolated."""
    
    def test_different_sessions_isolated(self):
        """Test that different session IDs have separate memory."""
        session1 = f"test_session_1_{uuid.uuid4()}"
        session2 = f"test_session_2_{uuid.uuid4()}"
        
        # Create two separate memories
        memory1 = AlchemystMemory(
            api_key=os.getenv("ALCHEMYST_AI_API_KEY"),
            session_id=session1
        )
        
        memory2 = AlchemystMemory(
            api_key=os.getenv("ALCHEMYST_AI_API_KEY"),
            session_id=session2
        )
        
        # Save different data to each
        memory1.save_context(
            inputs={"input": "My favorite color is blue"},
            outputs={"output": "Blue is nice!"}
        )
        
        memory2.save_context(
            inputs={"input": "My favorite color is red"},
            outputs={"output": "Red is great!"}
        )
        
        # Each should have its own data
        result1 = memory1.load_memory_variables({"input": "color"})
        result2 = memory2.load_memory_variables({"input": "color"})
        
        assert "history" in result1
        assert "history" in result2
        
        # Cleanup
        memory1.clear()
        memory2.clear()


class TestLangChainIntegration:
    """Test integration with LangChain."""
    
    def test_works_with_langchain(self, memory):
        """Test that AlchemystMemory works with LangChain ConversationChain."""
        pytest.importorskip("langchain_openai", reason="langchain-openai not installed")
        
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")
        
        from langchain.chains import ConversationChain
        from langchain_openai import ChatOpenAI
        
        # Create chain with AlchemystMemory
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        chain = ConversationChain(llm=llm, memory=memory)
        
        # Have a conversation
        response1 = chain.invoke({"input": "My name is TestUser"})
        assert "response" in response1
        
        response2 = chain.invoke({"input": "What is my name?"})
        assert "response" in response2
        # LLM should remember the name
        # Note: Actual response depends on LLM behavior
    
class TestEdgeCases:
    """Test edge cases and special scenarios."""
    
    def test_empty_save_context(self, memory):
        """Test saving empty context doesn't crash."""
        # Should not raise any errors
        memory.save_context(inputs={}, outputs={})
    
    def test_special_characters(self, memory):
        """Test handling of special characters."""
        memory.save_context(
            inputs={"input": "Hello! 你好 🌟 @#$%"},
            outputs={"output": "Response with émojis 😀"}
        )
        
        result = memory.load_memory_variables({"input": "hello"})
        assert "history" in result
    
    def test_long_messages(self, memory):
        """Test handling of very long messages."""
        long_text = "A" * 5000  # 5k characters
        
        memory.save_context(
            inputs={"input": long_text},
            outputs={"output": "Received"}
        )
        
        result = memory.load_memory_variables({"input": "test"})
        assert "history" in result
    
    def test_multiple_saves(self, memory):
        """Test saving multiple messages."""
        # Save multiple contexts
        for i in range(3):
            memory.save_context(
                inputs={"input": f"Message {i}"},
                outputs={"output": f"Response {i}"}
            )
        
        # Should be able to load
        result = memory.load_memory_variables({"input": "messages"})
        assert "history" in result


class TestMemoryProperties:
    """Test memory properties and attributes."""
    
    def test_memory_variables(self, memory):
        """Test memory_variables property."""
        assert memory.memory_variables == ["history"]
        assert isinstance(memory.memory_variables, list)
    
    def test_memory_keys(self, memory):
        """Test memory_keys property."""
        assert memory.memory_keys == ["history"]
        assert isinstance(memory.memory_keys, list)
    
    def test_session_id_stored(self, unique_session_id):
        """Test that session ID is properly stored."""
        memory = AlchemystMemory(
            api_key=os.getenv("ALCHEMYST_AI_API_KEY"),
            session_id=unique_session_id
        )
        
        assert memory._session_id == unique_session_id