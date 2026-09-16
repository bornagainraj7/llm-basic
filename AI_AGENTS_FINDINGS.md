# AI Agent Model Findings

## Context

I recently started following an AI Agents playlist and, this time, implemented and tested what was taught instead of only watching the lessons.

These observations come from approximately **1 to 1.5 hours of runtime testing**. They focus on model behavior during tool calling, not on errors in the Python code.

> **TL;DR:** Model output can vary significantly between providers and between runs with the same provider. Models may repeat a tool call, skip a step, call an unknown tool, or generate part of the plan themselves instead of following every step in the system prompt.

## Experiment Setup

### Typical prompts

- What can I do today in `{city}`?
- Should I go out in `{city}`?
- What activities can I do in `{city}`?

For some tests, I provided only the city name because that was the value the model was extracting for the first tool call.

### Cities tested

Mumbai, Vizag, Jaipur, Coimbatore, and Delhi.

### Tool sequence

The agent was expected to call these tools in order:

1. `weather(city)`
2. `activity(weather)`
3. `calorie_estimates(activity)`

### Local hardware

- **Laptop:** ASUS TUF
- **CPU:** Intel Core i7-12700H
- **Memory:** 16 GB DDR5 4800 MT/s
- **GPU:** Laptop NVIDIA RTX 3060 with 6 GB VRAM
- **Quantization:** Q4 models
- **Runtime:** LM Studio

## Summary

| Model | Type | Observed behavior | Overall result |
| --- | --- | --- | --- |
| Gemini 3.5 Flash Lite | Cloud | Usually followed the sequence, but sometimes repeated the first tool or skipped the calorie step | Best cloud experience in this experiment |
| GPT-5 Nano | Cloud | Frequently repeated the first tool and rarely continued to the second tool; often generated the remaining plan itself | Less reliable for this workflow |
| DeepSeek-R1 8B | Local | Slowest model; sometimes completed the sequence, but often repeated steps, skipped the final step, or called unknown tools | Successful in roughly 20–30% of runs |
| Llama 3.2 3B | Local | Fast after loading, but repeatedly called the first tool and produced unknown tool calls | Fast but unusable for this workflow |
| Gemma 4 E4B IT QAT | Local | Usually completed the sequence and produced a final answer, with occasional repeated calls | Best overall result in this experiment |

## Findings by Model

### 1. Google Gemini

**Model:** `gemini-3.5-flash-lite`

Gemini usually followed the steps defined in the system prompt. However, it sometimes:

- Skipped the final `calorie_estimates` step
- Called the first tool more than once
- Repeated the first tool two or three times

I tried improving the system prompt to make the sequence more explicit. This helped most of the time, but the first tool was still repeated in approximately 10% of runs.

Overall, Gemini provided the best experience among the cloud models tested.

### 2. OpenAI

**Model:** `gpt-5-nano`

GPT-5 Nano behaved very differently from Gemini. It frequently stopped after the first tool call and often repeated that call. Changes to the system prompt did not consistently solve the problem.

In several runs, the model:

- Repeated the first tool call multiple times
- Rarely continued to the `activity` tool
- Generated the rest of the plan without calling the remaining tools
- Questioned or contradicted the result returned by a tool
- Suggested additional planning instead of following the required sequence

Providing only the city name sometimes worked better than providing the complete natural-language prompt, because the model could use the city directly for its first tool call.

OpenAI also took longer than Gemini to respond at each step in this tool-calling workflow.

At this stage, Gemini's occasional skipped or repeated step was still a better result than GPT-5 Nano's behavior for this particular agent design.

### 3. DeepSeek-R1

**Model:** `deepseek-r1 8B`

DeepSeek-R1 was the slowest model tested. When I provided only a city name, its reasoning showed that it was uncertain about what to do with the short input. It still recognized that it should use the tools in many runs.

When I used the usual complete prompts, it often:

- Repeated the first tool call
- Skipped the final tool call
- Called a tool that did not exist, resulting in an unknown-tool response

It completed the full tool sequence and produced a final output in approximately 20–30% of runs.

### 4. Llama 3.2

**Model:** `llama-3.2-3b`

Llama 3.2 was the fastest local model after loading, but it performed the worst for this workflow.

During one run, it called the first tool almost 20 times before I stopped the process with `Ctrl+C`. Later runs showed similar behavior, including repeated first-tool calls and unknown tools.

It was fast, but it did not produce a reliable final result.

### 5. Gemma 4

**Model:** `unsloth/gemma-4-e4b-it-qat`

Gemma 4 produced the strongest local results in this experiment. In the first run, it completed the tool sequence and generated the final output without repeatedly calling the same tool.

In later runs:

- One run repeated the first tool twice but still completed successfully
- Another run completed each tool step once
- Response time was close to Llama 3.2, but with much better results

Gemma 4 was the best overall choice for my hardware because it ran locally, avoided API token usage, and still produced reasonably consistent tool-calling behavior.

## Overall Conclusions

1. A detailed system prompt does not guarantee that a model will follow a fixed tool sequence.
2. Tool-calling behavior varies between model families and between individual runs.
3. Larger or cloud-hosted models are not automatically better for a specific agent workflow.
4. A model may repeat a tool, skip a tool, invent a tool, or answer directly instead of following the orchestration logic.
5. Local models can be a practical option when token cost and API usage are concerns, but model selection matters greatly.
6. For this experiment, Gemini was the strongest cloud model and Gemma 4 was the strongest local model.

## Limitations

This was an informal experiment rather than a controlled benchmark. The number of runs was small, and the results may change with different prompts, model versions, sampling settings, context sizes, hardware, or tool definitions.

I also considered testing `gpt-oss 20b`, but decided not to run it because it would likely make the laptop unresponsive with the available hardware.

## Related Code

The implementation for these experiments is available here:

<https://github.com/bornagainraj7/llm-basic>