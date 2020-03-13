(*=======================================================-*-tuareg-*-======
 *
 * MGS : a general model of systems
 *
 *    Olivier Michel      : michel@lami.univ-evry.fr
 *    Jean-Louis Giavitto : giavitto@lami.univ-evry.fr
 *    Antoine Spicher     : aspicher@lami.univ-evry.fr
 *    Mailing-list        : mgs@lami.univ-evry.fr
 *    WWW                 : http://mgs.lami.univ-evry.fr
 *
 * LaMI umr 8042 du CNRS, Genopole (C), Universite d'Evry Val d'Essonne
 *
 *
 * -------------------------------------------------------------------
 * File: $RCSfile: array2D.ml,v $
 * Symbolic name : $Name:  $
 * Author: OM, JLG
 * Modified: $Date: 2013-01-16 18:23:06 $
 * Version: $Revision: 1.4 $
 * -------------------------------------------------------------------
 *
 * Status:  
 *     Représentation des tableaux à 2 dimensions
 *
 *=========================================================================
 *)

type 'a array2D = { row: int; col: int; data: 'a array; }



let row m = m.row
let col m = m.col
let data m = m.data
let get m i j =
  assert(
    if not ((0<=i)&&(i<(row m))&&(0<=j)&&(j<(col m))) then raise (Invalid_argument "Array2D: get: index out of bounds");
    true
  );
  (data m).(i * (col m) + j)
let set m i j v = 
  assert(
    if not ((0<=i)&&(i<(row m))&&(0<=j)&&(j<(col m))) then raise (Invalid_argument "Array2D: set: index out of bounds");
    true
  );
  (data m).(i * (col m) + j) <- v

let get m i j =
  assert(
    if not ((0<=i)&&(i<(row m))&&(0<=j)&&(j<(col m))) then raise (Invalid_argument "Array2D: get: index out of bounds");
    true
  );
  (data m).(i * (col m) + j)

let get_row m i =
  assert(
    if not ((0<=i)&&(i<(row m))) then raise (Invalid_argument "Array2D: get_row: index out of bounds");
    true
  );
  Array.init (col m) (fun j -> get m i j)

let get_col m j =
  assert(
    if not ((0<=j)&&(j<(col m))) then raise (Invalid_argument "Array2D: get_col: index out of bounds");
    true
  );
  Array.init (row m) (fun i -> get m i j)

let init r c f =
  assert(
    if not ((r>=0) && (c>=0)) then raise (Invalid_argument "Array2D: init: invalid bound");
    true
  );
  { row=r; col=c; data=(Array.init (r*c) (fun n -> f (n/c) (n mod c))) }

let make r c v = init r c (fun i j -> v)

let copy m = init (row m) (col m) (fun i j -> get m i j)

let of_array a =
  let l = Array.length a in
    if l = 0 then { row = 0; col = 0; data = a } else { row = l; col = 1; data = a }

let to_array m =
  assert(m.col = 1);
  m.data

let rec subminor m i j =
  let fill_subminor m' m xi xj =
    let ii = ref 0 in
    let jj = ref 0 in
      for i = 0 to (row m)-1 do
	if (i != xi)
	then (
	  jj := 0;
	  for j = 0 to (col m)-1 do
	    if (j != xj)
	    then (
	      set m' !ii !jj (get m i j);
	      jj := !jj + 1
	    )
	  done;
	  ii := !ii + 1
	)
      done
  in
    assert(
      if not ((0<=i)&&(i<(row m))&&(0<=j)&&(j<(col m))) then raise (Invalid_argument "Array2D: subminor: invalid bound") ;
      true
    );
    try
      let m' = init ((row m)-1) ((col m)-1) (fun _ _ -> get m i j) in
	fill_subminor m' m i j ;
	m'
    with Invalid_argument s -> raise (Invalid_argument (Printf.sprintf "Array2D: subminor: from '%s'" s))
      
let iteri f m starti startj =
  try
    for i = starti to ((row m)-1) do
      for j = startj to ((col m)-1) do
	f i j (get m i j)
      done
    done
  with Invalid_argument s -> raise (Invalid_argument (Printf.sprintf "Array2D: iteri: from '%s'" s))
    
let iter f m starti startj = iteri (fun _ _ v -> f v) m starti startj
                               
let iteri_row f m starti startj =
  try
    for j = startj to ((col m)-1) do
      f j (get m starti j)
    done
  with Invalid_argument s -> raise (Invalid_argument (Printf.sprintf "Array2D: iteri_row: from '%s'" s))
    
let iter_row f m starti startj = iteri_row (fun _ _ v -> f v) m starti startj

let iteri_col f m starti startj =
  try
    for i = starti to ((row m)-1) do
      f i (get m i startj)
    done
  with Invalid_argument s -> raise (Invalid_argument (Printf.sprintf "Array2D: iteri_col: from '%s'" s))
    
let iter_col f m starti startj = iteri_col (fun _ _ v -> f v) m starti startj
                                   
let mapi f m =
  try
    init (row m) (col m) (fun i j -> f i j (get m i j))
  with Invalid_argument s -> raise (Invalid_argument (Printf.sprintf "Array2D: mapi: from '%s'" s))
    
let map f m = mapi (fun _ _ v -> f v) m
                
let fold_left f z m = Array.fold_left f z (data m)
                        
let fold_right f m z = Array.fold_right f (data m) z
                         
let transpose m =
  init (col m) (row m) (fun i j -> get m j i)
    
let swap_row m i j =
  for k = 0 to (col m)-1 do
    let tmp = get m i k in
      set m i k (get m j k);
      set m j k tmp
  done
  
let swap_col m i j =
  for k = 0 to (row m)-1 do
    let tmp = get m k i in
      set m k i (get m k j);
      set m k j tmp
  done

let to_string string_of_elt m =
  let a = map string_of_elt m in
  let len = fold_left (fun acc s -> max acc (String.length s)) 0 a in
  let a = map (fun s -> let ss = String.make len ' ' in
		 String.blit s 0 ss (len-(String.length s)) (String.length s) ;
		 ss
	      ) a in
  let ret = ref "|" in
    for i = 0 to (row m)-1 do
      if (i!=0) then ret := Printf.sprintf "%s\n|" !ret;
      for j = 0 to (col m)-1 do
	if (j != 0)
	then ret := Printf.sprintf "%s %s" (!ret) (get a i j)
	else ret := Printf.sprintf "%s%s" (!ret) (get a i j)
      done;
      ret := Printf.sprintf "%s|" !ret
    done;
    if (row m = 0) then "||" else !ret


let append a =
  assert(
    let ok = ref true in
      for i = 0 to ((Array.length a)-1) do
	ok := !ok && ((col a.(i)) = (col a.(0)))
      done;
      if not !ok then raise (Invalid_argument "Array2D: append: dimensions mismatched");
      true;
  );
  { row = Array.fold_right (fun m acc -> acc + (row m)) a 0;
    col = (col a.(0));
    data = Array.concat (Array.to_list (Array.map data a));
  }

let concat m =
  let sz = map (fun m_ij -> row m_ij, col m_ij) m in
    assert(
      let ok = ref true in
	for i = 0 to ((row m)-1) do
	  for j = 0 to ((col m)-1) do
	    ok := !ok && (
	      let (nb_row, nb_col) = get sz i j
	      and (nb_row', _) = get sz i 0
	      and (_, nb_col') = get sz 0 j in
		(nb_row = nb_row') && (nb_col = nb_col')
	    )
	  done
	done;
	if not !ok then raise (Invalid_argument "Array2D: concat: dimensions mismatched");
	true
    );
    transpose
      (append
	 (Array.init (col m)
	    (fun j -> transpose
	       (append
		  (Array.init (row m) (fun i -> get m i j))))))

let sub m starti startj leni lenj =
  assert(
    if   (starti < 0) || (startj < 0) || (starti >= (row m)) || (startj >= (col m))
      || (leni > (row m) - starti) || (lenj > (col m) - startj) || (leni <= 0) || (lenj <= 0)
    then raise (Invalid_argument "Array2D: sub: invalid specification");
    true
  );
  init leni lenj (fun i j -> get m (starti+i) (startj+j))
;;



(*
let m = init 2 2 (fun i j -> match (i,j) with
		    | (0,0) -> init 3 5 (fun i j -> i * j)
		    | (0,1) -> init 3 1 (fun i j -> 7)
		    | (1,0) -> init 1 5 (fun i j -> 9)
		    | (1,1) -> init 1 1 (fun i j -> 1)
		 ) in
let m' = concat m in
  Printf.printf "%s\n\n" (to_string (to_string string_of_int) m);
  Printf.printf "%s\n\n" (to_string string_of_int m');
  Printf.printf "%s\n\n" (to_string string_of_int (sub m' 1 1 3 1))
;;

Printf.printf "%s\n" (to_string string_of_int (append [| (init 3 5 (fun i j -> i * j)); (init 1 5 (fun i j -> 9)) |] )) ;;
*)
