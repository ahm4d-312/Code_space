fn main() {
    //println!("\x1B[H\x1B[2J\x1B[3J");
    let days: [&str; 12] = [
        "First",
        "Second",
        "Third",
        "Fourth",
        "Fifth",
        "Sixth",
        "Seventh",
        "Eighth",
        "Ninth",
        "Tenth",
        "Eleventh",
        "Twelfth",
    ];
    let prizes: [&str; 12] = [
        "Partridge in a Pear Tree",
        "Turtle Doves",
        "French Hens",
        "Calling Birds",
        "Golden Rings",
        "Geese A-Laying",
        "Swans A-Swimming",
        "Maids A-Milking",
        "Ladies Dancing",
        "Lords A-Leaping",
        "Pipers Piping",
        "Drummers Drumming",
    ];

    for i in 1..13 {
        println!("The {} day prizes", days[i-1]);
        for ii in (0..i).rev() {
            println!("\t{}. {}", ii+1,prizes[ii])
        }
        println!("")
    }
}

/*
Partridge in a Pear Tree
Turtle Doves
French Hens
Calling Birds
Golden Rings
Geese A-Laying
Swans A-Swimming
Maids A-Milking
Ladies Dancing
Lords A-Leaping
Pipers Piping
Drummers Drumming
*/
