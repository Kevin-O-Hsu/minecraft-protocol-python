from abc import ABC, abstractmethod

class DataStruct(ABC):
    
    def __init__(self, *,  bytes_content:bytes=bytes(), data_content:tuple=tuple()) -> None:
        
        assert True in [bool(item) for item in (bytes_content, data_content)]
        
        
        self.bytes_content = bytes_content
        self.data_content = data_content
        
        if self.bytes_content == bytes():
            self.bytes_content = self.data_encode(self.data_content)
        elif self.data_content == tuple():
            self.data_content = self.data_decode(self.bytes_content)

    @abstractmethod
    def data_decode(self, bytes_content:bytes) -> tuple:
        """
        Override this method to convert bytes_content to data_content
        """
        pass

    @abstractmethod
    def data_encode(self, data_content:tuple) -> bytes:
        """
        Override this method to convert data_content to bytes_content
        """
        pass
