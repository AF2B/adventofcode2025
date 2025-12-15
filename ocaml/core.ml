let normalize_input input = 
  String.map (fun c -> 
    match c with
    | '\n' | '\r' | ' ' -> ','
    | _ -> c
    ) input

let extract_number input index = 
  let value = List.nth input index in
  let number_part = 
    String.sub value 1 (String.length value - 1) in
  int_of_string number_part

let read_line_path path =
  let open_ic = Stdlib.open_in path in
  let buffer = Buffer.create 1024 in
  try
    while true do
      let line = Stdlib.input_line open_ic in
      Buffer.add_string buffer line;
      Buffer.add_char buffer '\n';
    done;
    assert false
  with End_of_file ->
    close_in open_ic;
    Buffer.contents buffer

  let parse_input input = 
  input
  |> normalize_input
  |> String.split_on_char ','
  |> List.map String.trim
  |> List.filter (fun s -> s <> "")

let rollet start_point inputs = 
  let limit_up = 99 in
  let limit_down = 0 in
  let rec aux actual_position pwd instruction_index =
    if instruction_index >= List.length inputs then
      pwd
    else
      let instruction = List.nth inputs instruction_index in
      let steps = extract_number inputs instruction_index in
      
      let delta = 
        match instruction.[0] with
        | 'R' -> steps
        | 'L' -> -steps
        | _ -> 0
      in

      let size = limit_up - limit_down + 1 in
      let new_position = 
        ((actual_position + delta) mod size + size) mod size
      in

      let new_pwd =
        if new_position = 0 then pwd + 1 else pwd
      in

      aux new_position new_pwd (instruction_index + 1)
    in
    aux start_point 0 0

let main =
  let data = read_line_path "./input.txt" in
  let clean_data = parse_input data in
  Printf.printf "Result: [%s]\n" (String.concat ", " clean_data);
  Printf.printf "Result number: %d\n" (extract_number clean_data 0);
  Printf.printf "Rollet result: %d\n" (rollet 50 clean_data);
  0