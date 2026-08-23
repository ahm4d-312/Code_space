use crossterm::event::read;
use std::io::{stdin, stdout, Write};
fn main() {
    println!("\x1B[H\x1B[2J\x1B[3J");
    loop {
        println!("Fahrenheit to Celsius converter:");
        println!("1) C -> F");
        println!("2) F -> C");
        println!("3) exit");
        print!("~> ");
        stdout().flush().unwrap();

        let mut option: String = String::new();
        stdin()
            .read_line(&mut option)
            .expect("Falied to read the option.");

        if option.trim() != "1" && option.trim() != "2" {
            return;
        }

        print!("Enter the tampratrue: ");
        stdout().flush().unwrap();

        let mut temprature: String = String::new();
        stdin()
            .read_line(&mut temprature)
            .expect("Failed to read the value.");

        let temprature: f32 = match temprature.trim().parse() {
            Ok(temprature) => temprature,
            Err(_) => {
                println!("Enter a valid temprature value!");
                return;
            }
        };

        let answer: &str;
        let result: f32 = {
            if option.trim() == "1" {
                answer = "Celsius to Fahrenheit";
                converter(temprature, true)
            } else {
                answer = "Fahrenheit to Celsius";
                converter(temprature, false)
            }
        };
        println!("Converted {temprature} from {answer}...");
        println!("Result: {result}");

        read().unwrap();
        println!("\x1B[H\x1B[2J\x1B[3J");
    }
}

fn converter(temprature: f32, option: bool) -> f32 {
    if option {
        //C->F
        return (temprature * 1.8) + 32.0;
    }
    // F->C
    return (temprature - 32.0) / 1.8;
}

