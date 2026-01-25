import torch

class VariableSortedHistoryPooling(torch.nn.Module):
    def __init__(self, n_samples: int, emb_dim: int):
        super(VariableSortedHistoryPooling, self).__init__()
        # n samples are n events, where it's consecutive events belonging to a given user
        # The n samples can be segmented into B users.
        self.emb = torch.nn.Embedding(n_samples, emb_dim)
    def forward(self, event_indices: torch.Tensor, offsets: torch.Tensor) -> torch.Tensor:
        event_embs = self.emb(event_indices)
        # diffs of cumulative offsets gives user lengths (number of events in history per user)
        user_lengths = offsets[1:] - offsets[:-1]
        user_ids = torch.repeat_interleave(torch.arange(len(user_lengths),
                                                        device=offsets.device), 
                                            user_lengths)
        target = torch.zeros(len(user_lengths), event_embs.shape[1], device=event_embs.device)
        target = target.scatter_add(dim=0, index=user_ids.unsqueeze(1).expand_as(event_embs), src=event_embs)
        return target / user_lengths.clamp(min=1).unsqueeze(1) 