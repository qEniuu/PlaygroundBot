use pyo3::prelude::*;
use log::debug;

#[pyfunction]
pub fn interpret(code: String, input: String, ops_limit: usize) -> String {
    let mut array: Vec<u8> = vec![0];
    let mut array_ptr: usize = 0;
    let mut code_ptr: usize = 0;
    let mut input_ptr: usize = 0;
    let code: Vec<char> = code.chars().collect();
    let input: Vec<char> = input.chars().collect();
    let mut output: String = String::new();
    let mut loop_stack: Vec<usize> = vec![];
    debug!("code {:?} input {:?} ops_limit {:?}", code, input, ops_limit);
    for _ in 0..ops_limit {
        if let Some(op) = code.get(code_ptr) {
            match op {
                '>' => {
                    array_ptr += 1;
                    if let None = array.get(array_ptr) {
                        array.push(0);
                    }
                },
                '<' => {
                    array_ptr -= 1;
                    if let None = array.get(array_ptr) {
                        array.insert(0, 0);
                        array_ptr += 1;
                    }
                },
                '[' => {
                    if array[array_ptr] != 0 {
                        loop_stack.push(code_ptr);
                    } else {
                        while code[code_ptr] != ']' {
                            code_ptr += 1;
                        }
                        code_ptr += 1;
                    }
                },
                ']' => {
                    if array[array_ptr] != 0 {
                        code_ptr = usize::try_from(*loop_stack.last().unwrap()).unwrap();
                    } else {
                        loop_stack.pop();
                    }
                },
                '.' => output.push(char::from(array[array_ptr])),
                ',' => {
                    if let Some(x) = input.get(input_ptr) {
                        array[array_ptr] = u8::try_from(input[input_ptr]).unwrap();
                        input_ptr += 1;
                    } else {
                        array[array_ptr] = 0;
                    }
                },
                '+' => array[array_ptr] += 1,
                '-' => array[array_ptr] -= 1,
                _ => {},
            }
            code_ptr += 1;
        } else {
            break;
        }
    }
    output
}
