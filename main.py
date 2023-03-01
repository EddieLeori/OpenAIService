from lib.utility import *
from app import OpenAIService

if __name__ == "__main__":
    openaiservice = OpenAIService()
    openaiservice.run()
    Log("OpenAIService close.")