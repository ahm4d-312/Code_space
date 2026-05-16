use std::cmp::Ordering;
use std::io::{self, Write};
fn main() {
    let secret_number: i32 = rand::random_range(1..=100);
    println!("Guess the number!");

    loop {
        let mut guess: String = String::new();
        print!("Please input your guess:");
        io::stdout().flush().unwrap();
        io::stdin()
            .read_line(&mut guess)
            .expect("Failed to read the line.");
        println!("You guessed {guess}");

        let guess: i32 = match guess.trim().parse() {
            Ok(guess) => guess,
            Err(_) => {
                println!("Enter a valid number!");
                continue;
            }
        };
        match guess.cmp(&secret_number) {
            Ordering::Equal => {
                println!("You win!");
                break;
            }
            Ordering::Greater => println!("Too big!"),
            Ordering::Less => println!("Too small!"),
        }
    }
}
