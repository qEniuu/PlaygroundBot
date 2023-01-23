use pyo3::prelude::*;

mod brainfuck;

fn brainfuck_module(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    let module = PyModule::new(py, "brainfuck")?;
    module.add_function(wrap_pyfunction!(brainfuck::interpret, m)?)?;
    m.add_submodule(module);
    py.import("sys")?.getattr("modules")?.set_item("supermodule.submodule", module)?;
    Ok(())
}

#[pymodule]
fn playground_bot(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    pyo3_log::init();
    brainfuck_module(py, m);
    Ok(())
}
