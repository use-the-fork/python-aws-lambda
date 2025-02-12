import pytest
from sqlalchemy import Column, Integer, String
from python_aws_lambda.model.base_model import BaseModel

class MockModel(BaseModel):
    __tablename__ = 'mock'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

@pytest.fixture
def mock_instance():
    return MockModel(id=1, name='Test')

def test_to_dict(mock_instance):
    """Test the to_dict method of BaseModel."""
    expected_dict = {'id': 1, 'name': 'Test'}
    assert mock_instance.to_dict() == expected_dict

def test_to_json(mock_instance):
    """Test the to_json method of BaseModel."""
    expected_json = '{"id": 1, "name": "Test"}'
    assert mock_instance.to_json() == expected_json
