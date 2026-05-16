- `cargo build`
  build the project and save it in target/debug/file.rs.
- `cargo run`
  build and run the project directly.
- `cargo check`
  check the code status without building it, its faster than `cargo build` making it convenient when you just want to check the status of the code.

- `cargo build --release`
  - The Command: Use `cargo build --release` to compile your project with optimizations turned on.

  - The Result: Your executable is stored in **target/release** instead of the usual **target/debug**.

  - The Trade-off: Runtime: The program runs significantly faster.
    - Compile Time: The compiler takes longer to finish because it’s working hard to optimize the machine code.

  - Development vs. Release:
    - Development: Use the default (debug) profile for a fast "code-compile-test" loop.
    - Release: Use the release profile for the final product you give to users.

  > [!quote] Benchmarking: Never benchmark your code using the debug build! Always use the release executable in target/release to get an accurate measurement of its true speed.

