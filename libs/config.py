import yaml
import re

class Config:
    def __init__(self) -> None:
        try:
            with open("config.yaml", "r") as f:
                self.data = yaml.safe_load(f)
                print("[CONFIG] Configuration file loaded - successfully!")
        except:
            self.data = {
                "BOTConfig": {
                    "TOKEN": "TOKEN_BOT"
                },
                "STEOSVOICEConfig": {
                    "TOKEN": "TOKEN_STEOS_VOICE"
                }
            }
            with open("config.yaml", "w") as f:
                yaml.dump(self.data, f, default_flow_style=False)
            print("[CONFIG] Change configuration file - config.yaml!")
            exit(1)
        self.check_config()
    
    def check_config(self) -> None:
        try:    
            if not(re.search("^[0-9]*:[a-zA-Z0-9_-]*$", self.data["BOTConfig"]["TOKEN"])):
                print(f"[CONFIG] Check TOKEN in BOTConfig")
                exit(1)

            if not(re.search("^[a-zA-Z0-9-]*$", self.data["STEOSVOICEConfig"]["TOKEN"])):
                print("[CONFIG] Check TOKEN in STEOSVOICEConfig!")
                exit(1)

        except Exception as e:
                print(f"[CONFIG] Problems in configuration file!\n{e}")
                exit(1)
    
    def get_token_tg(self) -> str:
        return self.data["BOTConfig"]["TOKEN"]
    
    def get_token_sv(self) -> str:
        return self.data["STEOSVOICEConfig"]["TOKEN"]

config = Config()