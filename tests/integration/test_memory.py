"""Integration tests for AlchemystMemory.

These tests verify AlchemystMemory works correctly with real API calls.
They require valid ALCHEMYST_AI_API_KEY in environment.

Run tests:
    pytest tests/integration/test_memory.py
"""

import os
import uuid
import time
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
        session_id=unique_session_id,
        org_id="default"
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
        assert memory._org_id == "default"
        assert memory.memory_variables == ["history"]
        assert memory.memory_keys == ["history"]
    
    def test_save_and_load_context(self, memory):
        """Test saving context and loading it back."""
        # Save some context
        memory.save_context(
            inputs={"input": "My name is Alice"},
            outputs={"output": "Nice to meet you, Alice!"}
        )
        
        # Short sleep to allow cloud indexing
        time.sleep(1)
        
        # Load the context
        result = memory.load_memory_variables({"input": "What is my name?"})
        
        # Should have history
        assert "history" in result
        assert isinstance(result["history"], str)
        assert len(result["history"]) > 0
    
    def test_clear_memory(self, memory):
        """Test clearing memory."""
        # Add some data
        memory.save_context(
            inputs={"input": "Remember this: test123"},
            outputs={"output": "I'll remember that"}
        )
        
        # Clear memory (uses fixed memory_id kwarg internally)
        memory.clear()
        
        # Create new memory instance with same session
        new_memory = AlchemystMemory(
            api_key=os.getenv("ALCHEMYST_AI_API_KEY"),
            session_id=memory._session_id
        )
        
        # Load should return empty string after clear
        result = new_memory.load_memory_variables({"input": "test"})
        assert result["history"] == ""


class TestMemoryPersistence:
    """Test that memory persists across instances."""
    
    def test_memory_persists_across_instances(self, unique_session_id):
        """Test that data persists when creating new instance with same session."""
        api_key = os.getenv("ALCHEMYST_AI_API_KEY")
        
        # First instance - save data
        memory1 = AlchemystMemory(api_key=api_key, session_id=unique_session_id)
        memory1.save_context(
            inputs={"input": "I like pizza"},
            outputs={"output": "Great choice!"}
        )
        
        time.sleep(1)
        
        # Second instance - should retrieve the data
        memory2 = AlchemystMemory(api_key=api_key, session_id=unique_session_id)
        result = memory2.load_memory_variables({"input": "What do I like?"})
        
        assert "history" in result
        assert "pizza" in result["history"].lower()
        
        memory2.clear()


class TestSessionIsolation:
    """Test that different sessions are isolated."""
    
    def test_different_sessions_isolated(self):
        """Test that different session IDs have separate memory."""
        api_key = os.getenv("ALCHEMYST_AI_API_KEY")
        session1 = f"test_session_1_{uuid.uuid4()}"
        session2 = f"test_session_2_{uuid.uuid4()}"
        
        memory1 = AlchemystMemory(api_key=api_key, session_id=session1)
        memory2 = AlchemystMemory(api_key=api_key, session_id=session2)
        
        memory1.save_context(
            inputs={"input": "My favorite color is blue"},
            outputs={"output": "Blue is nice!"}
        )
        
        memory2.save_context(
            inputs={"input": "My favorite color is red"},
            outputs={"output": "Red is great!"}
        )
        
        time.sleep(1)
        
        result1 = memory1.load_memory_variables({"input": "color"})
        result2 = memory2.load_memory_variables({"input": "color"})
        
        assert "blue" in result1["history"].lower()
        assert "red" in result2["history"].lower()
        assert "red" not in result1["history"].lower()
        
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
        
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        chain = ConversationChain(llm=llm, memory=memory)
        
        chain.invoke({"input": "My name is TestUser"})
        time.sleep(1)
        response2 = chain.invoke({"input": "What is my name?"})
        
        assert "TestUser" in response2["response"]


class TestEdgeCases:
    """Test edge cases and special scenarios."""
    
    def test_empty_save_context(self, memory):
        """Test saving empty context doesn't crash."""
        memory.save_context(inputs={}, outputs={})
    
    def test_special_characters(self, memory):
        """Test handling of special characters."""
        memory.save_context(
            inputs={"input": "Hello! 你好 🌟 @#$%"},
            outputs={"output": "Response with émojis 😀"}
        )
        time.sleep(1)
        result = memory.load_memory_variables({"input": "hello"})
        assert "history" in result


class TestMemoryProperties:
    """Test memory properties and attributes."""
    
    def test_memory_variables(self, memory):
        """Test memory_variables property."""
        assert memory.memory_variables == ["history"]
    
    def test_memory_keys(self, memory):
        """Test memory_keys property."""
        assert memory.memory_keys == ["history"]