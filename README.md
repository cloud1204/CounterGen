# CounterGen

CounterGen is an LLM-assisted platform that helps problem solvers automatically generate counter-examples for buggy programs.

![Demo](./images/demo.png)

## Motivation

As every programmer knows, a counter-example is one of the most effective tools for debugging. However, many competitive programming platforms only provide a simple "Wrong Answer" verdict without showing the actual failing testcase.

Even when a failing testcase is provided, it is often a large, randomized input that is difficult for humans to interpret. This leaves problem solvers without meaningful insights to fix their code.

Our goal is to provide coders with minimal, human-readable counter-examples that immediately highlight the bugs.

## Project description

CounterGen leverages LLM APIs (Gemini, Claude, and OpenAI) to automatically generate and execute programs that perform stress testing against user submissions.

We have also designed an automated workflow to test these generated programs in every stage, ensuring they function as intended.

The workflow is summarized in the following diagram:

![Workflow](./images/workflow.png)

## How To Use

### Prerequisite Environment

* Python 3.9+

* g++ is required to run C++ programs provided by user.

### API Key

You would need a API key to enable LLM supports.
We supports 3 options: Gemini, Claude and openAI.

It is recommended to try Gemini first cause it offers a free plan: [Get Gemini API Key](https://aistudio.google.com/apikey)

### Setup Guide

1. Clone the repository
```
git clone https://github.com/cloud1204/CounterGen.git
cd CounterGen
```
2. (Optional) Create virtual environment
```
python3 -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate.bat     # Windows
```
3. Install Dependencies
```
pip install -r requirements.txt
```
4. Run the UI
```
python UI.py
```