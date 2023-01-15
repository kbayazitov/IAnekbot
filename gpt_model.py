import torch
from transformers import GPT2Tokenizer
import numpy as np
import wget

device = torch.device('cpu')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
URL = 'https://www.dropbox.com/s/4t618hm3tm6q0t2/gpt2_joke_model.pt?dl=1'
response = wget.download(URL)
model = torch.load(response, map_location=torch.device('cpu')) 


def choose_from_top(probs, n=5):
    ind = np.argpartition(probs, -n)[-n:]
    top_prob = probs[ind]
    top_prob = top_prob / np.sum(top_prob) 
    choice = np.random.choice(n, 1, p = top_prob)
    token_id = ind[choice][0]
    return int(token_id)

def generate_joke(input_str, text_len = 250):

    with torch.no_grad():      
        joke_finished = False
        cur_ids = torch.tensor(tokenizer.encode(input_str)).unsqueeze(0).to(device)

        for i in range(text_len):
            outputs = model(cur_ids, labels=cur_ids)
            loss, logits = outputs[:2]
            softmax_logits = torch.softmax(logits[0,-1], dim=0) 
            if i < 3:
                n = 20
            else:
                n = 3
            next_token_id = choose_from_top(softmax_logits.to('cpu').numpy(), n=n)
            cur_ids = torch.cat([cur_ids, torch.ones((1,1)).long().to(device) * next_token_id], dim = 1) 

            if next_token_id in tokenizer.encode('<|endoftext|>'):
                joke_finished = True
                break

            
        if joke_finished:             
            output_list = list(cur_ids.squeeze().to('cpu').numpy())
            output_text = tokenizer.decode(output_list)
            return output_text[:-13]