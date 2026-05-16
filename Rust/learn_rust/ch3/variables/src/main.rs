use std::io;
const SECONDS_IN_A_MONTH: i32 = 30 * 24 * 60 * 60;
fn main() {
    let x = 5;
    let x = x + 1;
    {
        let x = x * 3;
        println!("The value of x in the inner scope is {x}")
    }
    println!("The value of x is {x}");
    print_seconds();

    let num_dec = 15;
    println!("Num={num_dec}");
    let num_hex = 0xf;
    println!("Num={num_hex}");
    let num_oct = 0o17;
    println!("Num={num_oct}");
    let num_bin = 0b1111;
    println!("Num={num_bin}");

    let byte = b'A';
    println!("{byte}");

    let float: f64 = 1337.0;
    println!("The float value is: {float}");
    let tuple: (i32, i64, char, f64) = (10, 10, 'a', 6.0);
    println!("tuple: {1}{0}", tuple.3, "First element is: ");

    let arr: [i64; 10] = [0; 10];
    println!("First elment {}", arr[0]);

    print_array();
}

fn print_seconds() {
    println!("The of amount of seconds in a month is: {SECONDS_IN_A_MONTH}");
}

fn print_array() {
    let a = [1, 2, 3, 4, 5];

    println!("Please enter an array index.");

    let mut index = String::new();

    io::stdin()
        .read_line(&mut index)
        .expect("Failed to read the line.");

    let index: usize = index
        .trim()
        .parse()
        .expect("Index entered was not a number!");

    let element = a[index];

    println!("The value of the element at index {index} is: {element}");
}
