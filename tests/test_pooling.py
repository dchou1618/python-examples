import torch
import pytest
from LLMs.torch_examples.pooling import VariableSortedHistoryPooling

def loop_pooling(emb, event_indices, offsets):
    pooled = []
    for i in range(len(offsets) - 1):
        start, end = offsets[i].item(), offsets[i + 1].item()
        user_embs = emb(event_indices[start:end])
        pooled.append(user_embs.mean(dim=0))
    return torch.stack(pooled, dim=0)


def test_variable_sorted_history_pooling():
    torch.manual_seed(0)

    # ----- Test configuration -----
    vocab_size = 50
    emb_dim = 8
    B = 4                   # number of users
    lengths = torch.tensor([3, 1, 4, 2])
    offsets = torch.cat([torch.tensor([0]), lengths.cumsum(0)])
    N = offsets[-1].item()

    event_indices = torch.randint(0, vocab_size, (N,))

    # ----- Model -----
    model = VariableSortedHistoryPooling(vocab_size, emb_dim)

    # ----- Forward passes -----
    out_vec = model(event_indices, offsets)
    out_loop = loop_pooling(model.emb, event_indices, offsets)

    # ----- Assertions -----
    assert out_vec.shape == (B, emb_dim)
    assert torch.allclose(out_vec, out_loop, atol=1e-6)
