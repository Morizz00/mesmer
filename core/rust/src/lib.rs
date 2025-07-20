use std::ffi::{CStr, CString};
use std::os::raw::c_char;

#[unsafe(no_mangle)]
pub unsafe extern "C" fn clean_audio(input: *const c_char) -> *const c_char {
    let c_str = unsafe {
        CStr::from_ptr(input)
    };

    let filename = match c_str.to_str() {
        Ok(s) => s,
        Err(_) => return CString::new("invalid path").unwrap().into_raw()
    };

    println!("Cleaned audio file: {}", filename);

    CString::new("cleaned").unwrap().into_raw()
}