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
 * File: $RCSfile: linear.ml,v $
 * Symbolic name : $Name:  $
 * Author: OM, JLG
 * Modified: $Date: 2013/01/21 02:36:09 $
 * Version: $Revision: 1.1 $
 * -------------------------------------------------------------------
 *
 * Status:  
 *
 *=========================================================================
 *)


open Array2D

type 'a vector = 'a array

type 'a matrix = 'a array2D

module Make(Coef:
  sig
    type t
      
    val to_string: t -> string (* string_of_num *)
    val compare: t -> t -> int (* compare_num *)

    val zero: t (* zero_num *)
    val one: t (* one_num *)

    val neg: t -> t (* minus_num *)
    val add: t -> t -> t (* (+/) *)
    val sub: t -> t -> t (* (-/) *)
    val mul: t -> t -> t (* ( */) *)
    val div: t -> t -> t (* quo_num *)
    val rem: t -> t -> t (* mod_num *)

    val abs: t -> t (* abs_num *)

  end
) = struct

  type t = Coef.t matrix

  let to_string m = Array2D.to_string Coef.to_string m

  exception Compare of int

  let compare m1 m2 =
    let d = (Array2D.row m2) - (Array2D.row m1) in
      if (d <> 0) then d
      else (
	let d = (Array2D.col m2) - (Array2D.col m1) in
	  if (d <> 0) then d
	  else (

	    try
	      for i = 0 to (Array2D.row m1)-1 do
		for j = 0 to (Array2D.col m1)-1 do
		  let d = compare (Array2D.get m1 i j) (Array2D.get m2 i j) in
		    if (d <> 0) then raise (Compare d)
		done
	      done;
	      0
	    with Compare d -> d
	  )
      )

  let (+/) = Coef.add
  let (-/) = Coef.sub
  let ( */) = Coef.mul
  let (</) a b = (Coef.compare a b < 0)
  let (=/) a b = (Coef.compare a b = 0)
  let (<>/) a b = (Coef.compare a b <> 0)


  let neg m = Array2D.map Coef.neg m

  let add m1 m2 =
    assert ((Array2D.row m1)=(Array2D.row m2) && (Array2D.col m1)=(Array2D.col m2));
    Array2D.init (Array2D.row m1) (Array2D.col m1) (fun i j -> (Array2D.get m1 i j) +/ (Array2D.get m2 i j))

  let sub m1 m2 =
    assert ((Array2D.row m1)=(Array2D.row m2) && (Array2D.col m1)=(Array2D.col m2));
    Array2D.init (Array2D.row m1) (Array2D.col m1) (fun i j -> (Array2D.get m1 i j) -/ (Array2D.get m2 i j))

  let mul m1 m2 =
    assert ((Array2D.col m1)=(Array2D.row m2));
    Array2D.init (Array2D.row m1) (Array2D.col m2) (fun i j ->
						      let r = ref Coef.zero in
							for k = 0 to (Array2D.col m1)-1 do
							  r := !r +/ ((Array2D.get m1 i k) */ (Array2D.get m2 k j))
							done ;
							!r)

  let mul_matvec m (v: Coef.t vector) = Array2D.to_array (mul m (Array2D.of_array v))

  let mul_vecmat (v: Coef.t vector) m = Array2D.to_array (Array2D.transpose (mul (Array2D.transpose (Array2D.of_array v)) m))

  let dot s m = Array2D.map (( */) s) m

  exception Break

  let smith (b:t) =
    let l    = init (row b) (row b) (fun i j -> if (i=j) then Coef.one else Coef.zero)
    and r    = init (col b) (col b) (fun i j -> if (i=j) then Coef.one else Coef.zero)
    and linv = init (row b) (row b) (fun i j -> if (i=j) then Coef.one else Coef.zero)
    and rinv = init (col b) (col b) (fun i j -> if (i=j) then Coef.one else Coef.zero)
    and a    = copy b
    and m    = (min (row b) (col b))
    in

    let display_state i t j =
      Printf.printf "== %i (%i) t = %i ==\n" i j t;
      Printf.printf "%s\n\n" (to_string l);
      Printf.printf "%s\n\n" (to_string a);
      Printf.printf "%s\n" (to_string r);
      Printf.printf "=======\n";
    in

    let add_alpha_row m alpha i j =
      for k = 0 to (col m)-1 do
	set m j k ((get m j k) +/ (alpha */ (get m i k)))
      done
    in

    let add_alpha_col m alpha i j =
      for k = 0 to (row m)-1 do
	set m k j ((get m k j) +/ (alpha */ (get m k i)))
      done
    in

    let step1 t =
      (* Step 1: find pivot / stop if no non null ij *)
      let piv = ref None
      and x = ref t
      and y = ref t
      and allzero = ref true
      in
      let ltpiv saij = match !piv with
	| None -> true
	| Some piv -> saij </ piv
      in
	iteri (fun i j aij ->
		 if (Coef.zero <>/ aij)
		 then (
		   allzero := false;
		   let saij = Coef.abs aij in
		     if ltpiv saij
		     then (
		       piv := Some saij;
		       x := i;
		       y := j
		     )
		 )
	      ) a t t;
	(*Printf.printf "Choosing a pivot %i: %s (%i,%i)\n" t (string_of_num (get a !x !y)) !x !y ; Pervasives.flush stdout ;*)
	if !allzero then raise Break ;
	if !x != t then (swap_row a !x t; swap_row l !x t; swap_col linv t !x) ;
	if !y != t then (swap_col a !y t; swap_col r !y t; swap_row rinv t !y)
    in

    let rec step2 t i =
      (* Step 2: Annulation of the tth column *)
      if i < (row a) then (
	let att = get a t t
	and ait = get a i t in
	let quo,rem = Coef.div ait att, Coef.rem ait att in
	  (*
	  Printf.printf "For element (adding & swapping row) %s (/%s) at (%i,%i)\n" (string_of_num ait) (string_of_num att) i t;
	  Printf.printf "  - quotient: %s\n" (string_of_num quo);
	  Printf.printf "  - remainder: %s\n" (string_of_num rem);*)
	  add_alpha_row a (Coef.neg quo) t i ;
	  add_alpha_row l (Coef.neg quo) t i ;
	  add_alpha_col linv (quo) i t ;
	  if (Coef.zero =/ rem)
	  then step2 t (i+1)
	  else (
	    swap_row a t i;
	    swap_row l t i;
	    swap_col linv t i;
	    step2 t i
	  )
      ) else step3 t (t+1)

    and step3 t j =
      (* Step 3: Annulation of the tth row *)
      if j < (col a) then (
	let att = get a t t
	and atj = get a t j in
	let quo, rem = Coef.div atj att, Coef.rem atj att in
	  (*
	  Printf.printf "For element (adding & swapping col) %s at (%i,%i)\n" (string_of_num atj) t j;
	  Printf.printf "  - quotient: %s\n" (string_of_num quo);
	  Printf.printf "  - remainder: %s\n" (string_of_num rem);
	  *)
	  add_alpha_col a (Coef.neg quo) t j ;
	  add_alpha_col r (Coef.neg quo) t j ;
	  add_alpha_row rinv (quo) j t ;
	  if (Coef.zero =/ rem)
	  then step3 t (j+1)
	  else (
	    swap_col a t j;
	    swap_col r t j;
	    swap_row rinv t j;
	    step2 t (t+1)
	  )
      )
    in

    let step4 t =
      (* Step 4: aij multiple of att *)
      let c = ref t in
      let att = get a t t in
	try
	  iteri (fun i j aij -> (*
                   Printf.printf "coucou: %i %i\n" i j ;
                   Printf.printf "        %s\n" (string_of_num aij);
                   Printf.printf "        %s\n" (string_of_num att);
                   Printf.printf "        %s\n" (string_of_num (Coef.rem aij att)); *)
                   if not(Coef.zero =/ (Coef.rem aij att))
                   then (c:=j;
                         raise Break)) a (t+1) (t+1) ;
	  true
	with Break -> (
	  add_alpha_col a Coef.one !c t ;
	  add_alpha_col r Coef.one !c t ;	  
	  add_alpha_row rinv (Coef.neg Coef.one) t !c ;	  
	  false
	)
    in

    let big_cpt = ref 0 in

    let rec big_step t =
      if t < m then (
        (*display_state !big_cpt t 0;*)
	step1 t;
        (*display_state !big_cpt t 1;*)
	step2 t (t+1);
        (*display_state !big_cpt t 2;*)
	step3 t (t+1);
        (*display_state !big_cpt t 3;*)
	let s4 = step4 t in
          (*display_state !big_cpt t 4;*)
	  incr big_cpt;
          if s4 then big_step (t+1) else big_step t
      )
    in

    let last_step () = ()
    in

      (try big_step 0 with Break -> ());
      last_step ();
      linv, l, a, r, rinv

end
;;





module OfNum =
struct
  open Number
	
  include Make(
    struct
      type t = num
      
      let to_string = string_of_num
      let compare = compare_num
		      
      let zero = zero_num
      let one = one_num
		  
      let neg = minus_num
      let add = add_num
      let sub = sub_num
      let mul = mult_num
      let div = quo_num
      let rem = mod_num
		  
      let abs = abs_num
    end)

  let to_int_matrix m = Array2D.map int_of_num m

  let to_big_int_matrix m = Array2D.map big_int_of_num m

  let of_int_matrix m = Array2D.map num_of_int m

  let of_big_int_matrix m = Array2D.map num_of_big_int m

end
;;


module OfInt =
struct
  include Make(
    struct
      type t = int
		 
      let to_string = string_of_int
      let compare = Pervasives.compare

      let zero = 0
      let one = 1
		  
      let neg n = -n
      let add = (+)
      let sub = (-)
      let mul = ( * )
      let div = Number.quo_int
      let rem = Number.mod_int

      let abs = Pervasives.abs
    end)

  let to_num_matrix m = OfNum.of_int_matrix m

  let of_num_matrix m = OfNum.to_int_matrix m

end
;;


module OfFloat =
struct
  include Make(
    struct
      type t = float
		 
      let to_string = string_of_float
      let compare = Pervasives.compare

      let zero = 0.
      let one = 1.
		  
      let neg n = -.n
      let add = (+.)
      let sub = (-.)
      let mul = ( *. )
      let div = ( /. )
      let rem a b = 0.

      let abs = Pervasives.abs_float
    end)

end
;;


