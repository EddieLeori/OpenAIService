from lib.utility import *
from open_ai_service import OpenAIService

if __name__ == "__main__":
    openaiservice = OpenAIService()
    openaiservice.run()
    Log("OpenAIService close.")