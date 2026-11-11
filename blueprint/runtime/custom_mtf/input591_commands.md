# Build 5.91 input admission evidence

Observed isolated terminal root: `D:\BBMA\MT4_CustomMTF_302_Unit`.
Full source staged at `m10-stage\blueprint\source\BBMA_EA.mq4`, with the three custom headers alongside it. This is not the primary terminal.

Full source compile used the isolated `metaeditor.exe`, `/compile:` with that absolute source path, and `/log:` pointing to `evidence\input591_compile.log`. Observed result: 0 errors, 0 warnings, 1077 msec.

The exact observed pure helper harness and runner are preserved at `blueprint/tests/custom_mtf/CustomInputHarness.mq4` and `run_input_native_g40.py`. The runner requires the existing isolated staging directory and `config\parser_green.ini`; it does not bootstrap a terminal or authorize trading. It compiles the harness and runs the default, invalid and unavailable presets sequentially. It is specific to the observed G40 layout.

Observed invocation: `py -3.12 D:\BBMA\custom_mtf_302_input_runtime.py`. The preserved runner is that file's content. Its completion marker only means the processes ended. PASS evidence is the three explicit `passed=true` rows in `input591_evidence.json`, not process exit alone. Harness source is hashed before any regeneration.

Source/header/harness hashes use UTF-8 after CRLF to LF normalization; EX4 hashes use raw bytes. Local source, input header and preserved harness match the G40 inputs. No full EA OnInit/runtime or orders were tested by this harness.
