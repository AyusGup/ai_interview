from torch import nn


class FineTunedWav2Vec2Model(nn.Module):
    def __init__(self, wav2vec2_model, output_size):
        super(FineTunedWav2Vec2Model, self).__init__()
        self.wav2vec2 = wav2vec2_model
        self.fc = nn.Linear(self.wav2vec2.config.hidden_size, output_size)

    def forward(self, x):
        # Ensure x is the right shape (batch_size, channels, height, width)
        if x.dim() != 2:
            raise ValueError(f"Expected 4D input, but got {x.dim()}D input")
        
        outputs = self.wav2vec2(x)
        out = outputs.hidden_states[-1]
        out = self.fc(out[:, 0, :])  # Get the first token representation and pass through FC
        return out