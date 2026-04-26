# Study Note: Roadmap for "The Rust Programming Language"

This book is structured as a progressive journey, transitioning between theoretical concept chapters and hands-on project chapters.

## 1. Book Structure & Philosophy
* **Sequential Learning:** Chapters generally build on one another.
* **Two Chapter Types:** * **Concept Chapters:** Deep dives into specific language features.
    * **Project Chapters (2, 12, 21):** Practical application of preceding concepts.
* **The "Meticulous" Path:** If you prefer granular detail before building, you can skip Chapter 2 (intro project) and head straight to Chapter 3/4 (fundamentals).

---

## 2. The Curriculum Roadmap

### Phase 1: The Fundamentals (Ch. 1–6)
* **Ch 1:** Tooling setup (Cargo) and basic workflow.
* **Ch 2 (Project):** Building a Number Guessing Game.
* **Ch 3:** Basic syntax and common programming concepts.
* **Ch 4:** **Ownership, Borrowing, and Lifetimes** (The core memory management model).

* **Ch 5 & 6:** Defining custom data structures with Structs and Enums.

### Phase 2: Organization & Error Handling (Ch. 7–9)
* **Ch 7:** Managing large projects (Modules and API privacy).
* **Ch 8:** Working with Standard Library collections (Vectors, Strings, Hash Maps).
* **Ch 9:** Dealing with failure (Panic vs. Recoverable errors).

### Phase 3: Abstractions & Testing (Ch. 10–14)
* **Ch 10:** Generics, Traits, and further depth on Lifetimes.
* **Ch 11:** Automated testing logic.
* **Ch 12 (Project):** Implementing a **`grep`** CLI tool.
* **Ch 13:** Functional features (Iterators and Closures).
* **Ch 14:** Advanced Cargo and library distribution.

### Phase 4: Systems Programming & Concurrency (Ch. 15–17)
* **Ch 15:** Smart Pointers (`Box`, `Rc`, `Arc`, `RefCell`).
* **Ch 16:** Fearless Concurrency (Threads and data sharing).
* **Ch 17:** Asynchronous programming (`async`/`await`, Futures, and Streams).


### Phase 5: Advanced Topics (Ch. 18–21)
* **Ch 18 & 19:** Patterns, Matching, and OOP comparisons.
* **Ch 20:** The "Dark Arts" (Unsafe Rust, Macros, and advanced Trait manipulation).
* **Ch 21 (Project):** Implementing a **Low-level Multithreaded Web Server**.

---

## 3. Learning Through Failure
The book intentionally includes code that will not compile to teach you how to interpret compiler diagnostics. 

**Ferris the Crab Indicators:**
* **Does not compile:** Used to demonstrate language constraints/safety.
* **Panics:** Code that compiles but crashes at runtime.
* **Does not produce desired behavior:** Logical errors or non-idiomatic code.



## 4. Reference Material (Appendixes)
* **A-C:** Keywords, Operators, and Derivable Traits.
* **D-E:** Development tools and a guide to **Rust Editions** (e.g., 2024 Edition).
* **G:** Background on how Rust is developed and the "Nightly" release cycle.
