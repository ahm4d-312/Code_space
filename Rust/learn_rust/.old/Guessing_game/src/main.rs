use std::io::{self, Write};
fn main() {
    print!("Guess a number:");
    io::stdout().flush().expect("Error no 101");
    let mut guess:String=String::new();
    io::stdin()
    .read_line(&mut guess)
    .expect("Failed to read the line");
    println!("You guessed: {guess}");
خ}