# Lab 2.8: Call Transfer

**Duration:** 45 minutes
**Level:** 2

## Objectives

Complete this lab to demonstrate your understanding of the concepts covered.

## Prerequisites

- Completed previous labs
- Python 3.10+ with signalwire-agents installed
- Virtual environment activated

## Instructions

### 1. Set Up Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Implement Your Solution

Edit `solution/agent.py` according to the lab requirements.

### 3. Test Locally

```bash
# List available functions
swaig-test solution/agent.py --list-tools

# Check SWML output
swaig-test solution/agent.py --dump-swml
```

### 4. Submit

```bash
git add solution/agent.py
git commit -m "Complete Lab 2.8: Call Transfer"
git push
```

## Grading

| Check | Points |
|-------|--------|
| Agent Instantiation | 15 |
| SWML Generation | 15 |
| transfer_to_department function | 20 |
| check_availability function | 15 |
| transfer_with_context function | 20 |
| Transfer uses connect() action | 15 |
| **Total** | **100** |

**Passing Score:** 70%

## Reference

See `reference/starter.py` for a boilerplate template.

---

## Next Assignment

Ready to continue? [**Start Lab 2.9: Multi-Agent Architecture**](https://classroom.github.com/a/wkFn4kfZ)

---

*SignalWire AI Agents Certification*
