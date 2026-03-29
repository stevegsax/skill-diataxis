import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def intro():
    import marimo as mo

    mo.md(
        """
        # Environment Check Exercise

        This exercise walks you through verifying that your local fine-tuning
        environment is correctly set up. Run each cell and check that the output
        matches expectations.
        """
    )
    return (mo,)


@app.cell
def check_python():
    import sys
    import marimo as mo

    version = sys.version_info
    status = "PASS" if version >= (3, 10) else "FAIL"
    color = "green" if status == "PASS" else "red"

    mo.md(
        f"""
        ## Step 1: Python Version

        **Result**: Python {version.major}.{version.minor}.{version.micro}

        **Status**: <span style="color: {color}; font-weight: bold;">{status}</span>

        Requirement: Python 3.10 or later.
        """
    )
    return (version, status)


@app.cell
def check_torch():
    import marimo as mo

    try:
        import torch

        torch_version = torch.__version__
        cuda_available = torch.cuda.is_available()
        cuda_version = torch.version.cuda if cuda_available else "N/A"
        gpu_name = torch.cuda.get_device_name(0) if cuda_available else "N/A"
        vram_gb = (
            f"{torch.cuda.get_device_properties(0).total_mem / 1e9:.1f} GB"
            if cuda_available
            else "N/A"
        )
        status = "PASS" if cuda_available else "WARN"
        color = "green" if status == "PASS" else "orange"

        mo.md(
            f"""
            ## Step 2: PyTorch and CUDA

            | Property | Value |
            |----------|-------|
            | PyTorch version | {torch_version} |
            | CUDA available | {cuda_available} |
            | CUDA version | {cuda_version} |
            | GPU name | {gpu_name} |
            | VRAM | {vram_gb} |

            **Status**: <span style="color: {color}; font-weight: bold;">{status}</span>

            {"GPU detected and ready." if cuda_available else "No GPU detected. Fine-tuning will be extremely slow on CPU."}
            """
        )
    except ImportError:
        mo.md(
            """
            ## Step 2: PyTorch and CUDA

            **Status**: <span style="color: red; font-weight: bold;">FAIL</span>

            PyTorch is not installed. Run: `pip install torch --index-url https://download.pytorch.org/whl/cu121`
            """
        )
    return ()


@app.cell
def check_libraries():
    import marimo as mo

    libraries = {
        "transformers": "transformers",
        "datasets": "datasets",
        "peft": "peft",
        "bitsandbytes": "bitsandbytes",
        "trl": "trl",
        "accelerate": "accelerate",
    }

    results = []
    for display_name, import_name in libraries.items():
        try:
            mod = __import__(import_name)
            version = getattr(mod, "__version__", "unknown")
            results.append((display_name, version, "PASS"))
        except ImportError:
            results.append((display_name, "not installed", "FAIL"))

    table_rows = "\n".join(
        f"| {name} | {ver} | {'PASS' if st == 'PASS' else 'FAIL'} |"
        for name, ver, st in results
    )

    all_pass = all(st == "PASS" for _, _, st in results)
    missing = [name for name, _, st in results if st != "PASS"]

    summary = (
        "All required libraries are installed."
        if all_pass
        else f"Missing libraries: {', '.join(missing)}. Install them with pip."
    )

    mo.md(
        f"""
        ## Step 3: Required Libraries

        | Library | Version | Status |
        |---------|---------|--------|
        {table_rows}

        {summary}
        """
    )
    return (results, all_pass)


@app.cell
def check_optional():
    import marimo as mo

    optional = {"unsloth": "unsloth"}
    opt_results = []
    for display_name, import_name in optional.items():
        try:
            mod = __import__(import_name)
            version = getattr(mod, "__version__", "unknown")
            opt_results.append((display_name, version, "INSTALLED"))
        except ImportError:
            opt_results.append((display_name, "not installed", "OPTIONAL"))

    opt_rows = "\n".join(
        f"| {name} | {ver} | {st} |" for name, ver, st in opt_results
    )

    mo.md(
        f"""
        ## Step 4: Optional Libraries

        | Library | Version | Status |
        |---------|---------|--------|
        {opt_rows}

        These are optional. Training works without them but may be slower.
        """
    )
    return ()


@app.cell
def vram_estimator():
    import marimo as mo

    model_size_slider = mo.ui.slider(
        start=1, stop=70, step=1, value=8, label="Model size (billions of parameters)"
    )
    batch_size_slider = mo.ui.slider(
        start=1, stop=8, step=1, value=4, label="Batch size"
    )

    mo.md(
        f"""
        ## Step 5: VRAM Estimator

        Use the sliders to estimate VRAM requirements for QLoRA training.

        {model_size_slider}

        {batch_size_slider}
        """
    )
    return (model_size_slider, batch_size_slider)


@app.cell
def vram_calculation(model_size_slider, batch_size_slider):
    import marimo as mo

    params_b = model_size_slider.value
    batch = batch_size_slider.value

    model_vram = params_b * 0.5  # 4-bit: ~0.5 GB per billion params
    lora_vram = params_b * 0.01  # LoRA adapters: ~1% of model
    optimizer_vram = lora_vram * 2  # Adam: 2x states
    activation_vram = batch * 0.5  # rough estimate per batch element
    total_vram = model_vram + lora_vram + optimizer_vram + activation_vram

    mo.md(
        f"""
        ### Estimated VRAM Breakdown

        | Component | Estimated VRAM |
        |-----------|---------------|
        | Base model (4-bit) | {model_vram:.1f} GB |
        | LoRA adapters | {lora_vram:.2f} GB |
        | Optimizer states | {optimizer_vram:.2f} GB |
        | Activations (batch={batch}) | {activation_vram:.1f} GB |
        | **Total** | **{total_vram:.1f} GB** |

        {"This should fit on your GPU." if total_vram < 24 else "This may require a GPU with 48+ GB VRAM. Consider a smaller model or batch size of 1."}
        """
    )
    return ()


@app.cell
def summary():
    import marimo as mo

    mo.md(
        """
        ## Summary

        If all checks above show PASS, your environment is ready for fine-tuning.
        Proceed to the [Dataset Preparation Tutorial](../tutorials/dataset-preparation.md).

        If any checks failed, refer to the
        [Environment Requirements Reference](../reference/environment-requirements.md)
        for troubleshooting.
        """
    )
    return ()


if __name__ == "__main__":
    app.run()
