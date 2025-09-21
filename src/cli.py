import argparse
import readline
import sys
from .deepseek_api import DeepSeekAPI
from .config import load_config

class DeepSeekCLI:
    def __init__(self):
        self.config = load_config()
        self.api = DeepSeekAPI(self.config['api_key'])
        self.conversation_history = []
        
    def print_banner(self):
        banner = """
        🤖 DeepSeek CLI Assistant
        Type 'quit', 'exit', or 'q' to exit
        Type 'clear' to clear conversation history
        Type 'stream' to toggle streaming mode
        """
        print(banner)
    
    def run(self):
        self.print_banner()
        streaming = False
        
        while True:
            try:
                user_input = input("👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                    
                elif user_input.lower() == 'clear':
                    self.conversation_history = []
                    print("🗑️ Conversation history cleared")
                    continue
                    
                elif user_input.lower() == 'stream':
                    streaming = not streaming
                    mode = "streaming" if streaming else "standard"
                    print(f"🔄 Mode changed to: {mode}")
                    continue
                
                if not user_input:
                    continue
                
                # Add user message to history
                self.conversation_history.append({"role": "user", "content": user_input})
                
                print("🤖 DeepSeek: ", end="", flush=True)
                
                if streaming:
                    response_text = ""
                    for chunk in self.api.stream_chat(self.conversation_history):
                        print(chunk, end="", flush=True)
                        response_text += chunk
                    print()
                    
                    # Add assistant response to history
                    self.conversation_history.append({"role": "assistant", "content": response_text})
                    
                else:
                    response = self.api.chat(self.conversation_history)
                    print(response)
                    
                    # Add assistant response to history
                    self.conversation_history.append({"role": "assistant", "content": response})
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                continue

def main():
    parser = argparse.ArgumentParser(description="DeepSeek CLI Assistant")
    parser.add_argument('--api-key', help='Your DeepSeek API key')
    
    args = parser.parse_args()
    
    cli = DeepSeekCLI()
    cli.run()

if __name__ == "__main__":
    main()
