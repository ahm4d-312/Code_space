fn main() {
    let a = Box::new([0; 1_000_000]);
    let b = &a;
    //println!("{}",a[0]);
let s;

    let first = String::from("Ferris");
    let full = add_suffix(first.clone());
    println!("{full}");
    println!("{first}");

}

fn add_suffix(mut name: String) -> String {
    name.push_str(" Jr.");
    return name;
}