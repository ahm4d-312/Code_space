use crossterm::event::read;
use std::io::{self, Write};

fn fib_loop(num: i64) -> i64 {
    let mut fib_pair: [i64; 2] = [0, 1];
    if num < 2 {
        return num;
    }
    for _ in 2..num {
        // xor swapping
        fib_pair[0] = fib_pair[0] ^ fib_pair[1];
        fib_pair[1] = fib_pair[0] ^ fib_pair[1];
        fib_pair[0] = fib_pair[0] ^ fib_pair[1];

        fib_pair[1] = fib_pair[0] + fib_pair[1];
    }
    return fib_pair[0] + fib_pair[1];
}

fn main() {
    println!("\x1B[H\x1B[2J\x1B[3J");
    loop {
        println!("Enter a number to choose a mode:");
        println!("1) Recursion mode");
        println!("2) For loop mode");
        println!("3) exit");
        print!("~> ");
        io::stdout().flush().unwrap();

        let mut option: String = String::new();
        io::stdin()
            .read_line(&mut option)
            .expect("Failed to write the number");

        if option.trim() != "1" && option.trim() != "2" {
            return;
        }

        print!("Enter the value: ");
        io::stdout().flush().unwrap();
        let mut num: String = String::new();
        io::stdin()
            .read_line(&mut num)
            .expect("Failed to write the number");

        let num: i64 = match num.trim().parse() {
            Ok(num) => num,
            Err(_) => {
                println!("Enter a valid number!");
                return;
            }
        };
        if option.trim() == "1" {
            //let fib_value: i64 = fib_sequence(num);
            //println!("The fib value of {num} is: {fib_value}");
            //println!("Note: The recursion mode was used.");
            println!("Not ready yet...");
            println!("Will be done soon.")
        } else {
            let fib_value: i64 = fib_loop(num);
            println!("The fib value of {num} is: {fib_value}");
            println!("Note: The loop mode was used.");
        }

        read().unwrap();
        println!("\x1B[H\x1B[2J\x1B[3J");
    }
}
