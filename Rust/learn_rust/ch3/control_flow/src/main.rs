fn main() {
    println!("Hello, world!");
    let num = 10;
    if num % 2 == 0 {
        println!("Num is Even")
    } else {
        println!("Num is Odd")
    }

    //a_loop();
    //another_loop();
    also_another_loop();
    println!();
    for_loop();
}

fn a_loop() {
    let mut count = 0;
    'counting_up: loop {
        println!("count = {count}");
        let mut remaining = 10;

        loop {
            println!("remaining = {remaining}");
            if remaining == 9 {
                break;
            }
            if count == 2 {
                break 'counting_up;
            }
            remaining -= 1;
        }

        count += 1;
    }
    println!("End count = {count}");
    println!("-------------------------")
}

fn another_loop() {
    let mut count = 0;
    'counter: loop {
        println!("count= {count}");
        let mut remaining = 3;
        loop {
            println!("remaining = {remaining}");
            if remaining == 1 {
                break;
            }
            if count == 2 {
                break 'counter;
            }
            remaining -= 1;
        }
        count += 1;
    }
    println!("End count = {count}");
}

fn also_another_loop() {
    let arr = [1, 2, 3, 4, 5];
    let mut i = 0;
    while i < 5 {
        println!("Value at index{i}= {}", arr[i]);
        i += 1;
    }
}

fn for_loop() {
    let arr = [10, 20, 30, 40, 50];

    for i in arr {
        println!("Value = {i}")
    }
    println!();
    for i in 1..4 {
        println!("{i}!");
    }
    println!("LIFTOFF!!!");
    println!();
    for i in (1..4).rev() {
        println!("{i}!");
    }
    println!("LIFTOFF!!!");
}
