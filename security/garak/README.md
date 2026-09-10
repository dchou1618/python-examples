# garak scans

This directory contains the repository's opt-in LLM security scan. garak sends
adversarial probes to a configured model and writes its reports under
`security/garak/reports/`.

## Run locally

Install the project environment, then provide the model adapter and model name:

```bash
uv sync
GARAK_MODEL_TYPE=openai GARAK_MODEL_NAME=gpt-4o-mini \
  ./security/garak/run_scan.sh
```

The default probe set is intentionally small for a quick smoke scan. Override
it with a comma-separated garak probe list when needed:

```bash
GARAK_PROBES=dan,promptinject,encoding \
  GARAK_MODEL_TYPE=openai GARAK_MODEL_NAME=gpt-4o-mini \
  ./security/garak/run_scan.sh
```

Provider credentials are read by garak from its normal environment variables;
do not put credentials in this repository. Common examples are `OPENAI_API_KEY`
and `HF_TOKEN`, depending on the selected model type.

## CI

The workflow is manual or scheduled and only performs a scan when the
repository has a `GARAK_MODEL_NAME` secret. Configure `GARAK_MODEL_TYPE`,
`GARAK_MODEL_NAME`, and any provider credential as repository secrets before
enabling it. CI permits a skipped scan when the model secret is absent.

Reports are ignored because they can contain prompts, model outputs, and other
sensitive data. Review the generated report locally or upload it through an
approved private artifact workflow if long-term retention is required.