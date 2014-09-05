#!/usr/bin/env python


def MissingTokens(Exception): 
    pass

def parse_with_tokens(strg,tokens):
    if len(tokens) < 0 or tokens == None:
        raise MissingTokens()

    else:
        command_dict = {}
        words = strg.split()
        command_dict["command"] = words.pop(0)
        token_active = None
        for word in words:
            if word  in tokens: #" ".join(tokens):
                
                token_active = word[:-1]
                command_dict[token_active] = ""
            else:
                if token_active:
                    command_dict[token_active] = " ".join([command_dict[token_active], word]).lstrip()

    return command_dict





