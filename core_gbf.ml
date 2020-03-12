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
 * File: $RCSfile: core_gbf.ml,v $
 * Symbolic name : $Name:  $
 * Author: OM, JLG
 * Modified: $Date: 2014/06/20 19:35:01 $
 * Version: $Revision: 1.15 $
 * -------------------------------------------------------------------
 *
 * Status:  
 *     Fonction de base sur les GBFs
 *
 *=========================================================================
 *)


open Global
open Def_gbf


module IntMatrix = Linear.OfInt ;;

module VectorSet = Set.Make(struct type t = int Linear.vector let compare = Pervasives.compare end) ;;

let internal_order tor c =
  let l = Array.length tor in
    Number.lcm_int_array
      (Array.mapi (fun i p ->
		     if (p = 0) then 1
		     else
		       if (i < l)
		       then let n = tor.(i) in abs (n / (Number.gcd_int p n))
		       else 0
		  ) c)

let internal_normalize tor c =
  Array.iteri (fun i m -> c.(i) <- Number.mod_int c.(i) m) tor;
  c

let info_presentation p =

  Printf.printf "relators:\n%s\n" (Linear.OfNum.to_string p.smith_spec.m);
  Printf.printf "rank: %d\n" p.rank;
  Printf.printf "order: %d\n" p.order;
  Printf.printf "torsions:\n%s\n" (IntMatrix.to_string (Array2D.of_array p.torsions));
  Printf.printf "of_graph:\n%s\n" (IntMatrix.to_string p.of_graph);
  Printf.printf "to_graph:\n%s\n" (IntMatrix.to_string p.to_graph);
  Printf.printf "degree: %d\n" p.degree;
  Printf.printf "orders:\n%s\n" (IntMatrix.to_string (Array2D.of_array p.orders)) ;
  ()
;;

let vector p c = c.(p.rank - 1) = 0

let point p c =  not(vector p c)

let order p c =
  assert(Array.length c = p.rank);
  internal_order p.torsions c

let normalize p c =
  assert(Array.length c = p.rank);
  internal_normalize p.torsions c



let generator p i =
  assert(i < p.degree);
  p.basis.(i)

let origin p = p.basis.(p.degree)

let zero p = Array.make p.rank 0

let add c1 c2 =
  assert(Array.length c1 = Array.length c2);
  Array.mapi (fun i -> (+) c1.(i)) c2

let sub c1 c2 =
  assert(Array.length c1 = Array.length c2);
  Array.mapi (fun i -> (-) c1.(i)) c2

let mul n c =
  Array.map (( * ) n) c

let neg c = mul (-1) c



let imp_generator p i =
  assert(i < p.degree);
  Array.copy (p.basis.(i))

let imp_origin p =
  Array.copy (p.basis.(p.degree))

let imp_zero p =
  zero p

let imp_add c1 c2 =
  assert(Array.length c1 = Array.length c2);
  Array.iteri (fun i x1 -> c1.(i) <- x1 + c2.(i)) c1;
  c1

let imp_addn c1 n c2 =
  assert(Array.length c1 = Array.length c2);
  Array.iteri (fun i x1 -> c1.(i) <- x1 + n * c2.(i)) c1;
  c1

let imp_sub c1 c2 =
  assert(Array.length c1 = Array.length c2);
  Array.iteri (fun i x1 -> c1.(i) <- x1 - c2.(i)) c1;
  c1

let imp_mul n c =
  Array.iteri (fun i x -> c.(i) <- n * x) c;
  c

let imp_neg c = imp_mul (-1) c






let to_point p c =
  let lst = p.rank - 1 in
    (match c.(lst) with
       | 1 -> ()
       | 0 -> ( c.(lst) <- 1 )
       | n -> (
	   if (n < 0) then Array.iteri (fun i x -> c.(i) <- (-x)) c;
	   let d = Number.gcd_int_array c in
	     if (d <> 1) then Array.iteri (fun i x -> c.(i) <- x / d) c
	 )
    );
    c

let neighbors p c =
  Array.map
    (fun d -> normalize p (add c d))
    p.neighbors

let neighbors_list p c = Array.to_list (neighbors p c)
                           
let iter_neighbors p f c =
  for i = 0 to (-1 + Array.length p.neighbors) do
    f (normalize p (add c p.neighbors.(i)))
  done

let fold_neighbors p f c z =
  let ret = ref z in
    for i = 0 to (-1 + Array.length p.neighbors) do
      ret := f (normalize p (add c p.neighbors.(i))) (!ret)
    done;
    !ret

let folddown_neighbors p f c z =
  let ret = ref z in
    for i = (-1 + Array.length p.neighbors) downto 0 do
      ret := f (normalize p (add c p.neighbors.(i))) (!ret)
    done;
    !ret
;;

let compare_graph p1 p2 =
  Pervasives.compare p1.id p2.id
;;






let create_presentation =
  try
    let id = ref 0 in
      fun d relators ->
	if List.exists (fun relator -> Array.length relator <> d) (Array.to_list relators)
	then raise (Erreur "Core_gbf: create_presentation: unable");
	
	let nb_rel = Array.length relators in
	  
	let m = IntMatrix.to_num_matrix (Array2D.init d nb_rel (fun i j -> relators.(j).(i))) in
	  
	let (linv, l, a, rinv, r) = Linear.OfNum.smith m in
	let smith_spec = {
	  m = m;
	  a = a;
	  l = l;
	  r = r;
	  l_inv = linv;
	  r_inv = rinv;
	} in
	let linv = IntMatrix.of_num_matrix linv
	and l = IntMatrix.of_num_matrix l
	and a = IntMatrix.of_num_matrix a
	in

	let signature = Array.init d (fun i -> if (i < nb_rel) then Array2D.get a i i else 0) in

	let (d_trivial, l_cyclic, d_free) =
	  Array.fold_right (fun p (t,c,f) ->
			      if (abs p = 1) then (t+1,c,f)
			      else if (p = 0) then (t,c,f+1)
			      else (t,p::c,f)
			   ) signature (0,[],0)
	in

	let d_cyclic = List.length l_cyclic in

	let torsions = Array.of_list l_cyclic in

	let order = if d_free > 0 then 0 else Array.fold_left ( * ) 1 torsions in

	let rank = d_cyclic + d_free + 1 in

	let of_graph =
	  Array2D.concat
	    (Array2D.init 2 2 (fun i j -> match (i,j) with
				 | (0,0) -> Array2D.sub l d_trivial 0 (rank-1) d
				 | (0,1) -> Array2D.make (rank-1) 1 0
				 | (1,0) -> Array2D.make 1 d 0
				 | (1,1) -> Array2D.make 1 1 1
				 | _ -> failwith "Core_gbf: create_presentation: internal error"
			      ))
	and to_graph =
	  Array2D.concat
	    (Array2D.init 2 2 (fun i j -> match (i,j) with
				 | (0,0) -> Array2D.sub linv 0 d_trivial d (rank-1)
				 | (0,1) -> Array2D.make d 1 0
				 | (1,0) -> Array2D.make 1 (rank-1) 0
				 | (1,1) -> Array2D.make 1 1 1
				 | _ -> failwith "Core_gbf: create_presentation: internal error"
			      ))
	in

	let basis = Array.init (d+1) (fun gen_index -> internal_normalize torsions (Array2D.get_col of_graph gen_index)) in

        let neighbors =
          let ret = ref VectorSet.empty in
            for i = 0 to d-1 do
              let gen_pos = basis.(i) in
              let gen_neg = internal_normalize torsions (neg gen_pos) in
                ret := VectorSet.add gen_pos (VectorSet.add gen_neg !ret)
            done;
            !ret
        in

	let orders = Array.sub (Array.map (internal_order torsions) basis) 0 d in

	  { id  = (incr id; !id);
	    smith_spec = smith_spec;

	    rank = rank;
	    torsions = torsions;
	    order = order;
	    of_graph = of_graph;
	    basis = basis;
            neighbors = Array.of_list (VectorSet.elements neighbors);

	    degree = d;
	    orders = orders;
	    to_graph = to_graph;
	  }

  with Failure("int_of_big_int") -> raise (Erreur "Core_gbf: create_presentation: too large intergers are involved in the presentation (32 bits integers are used instead of numbers with arbitrary precision for efficiency)")
;;





































let empty_field () = Hash.create 17

let unsafe_set (f: 'a cayley_field) (c: cayley_cell) (d: 'a) =
  Hash.replace f c d

let unsafe_get (f: 'a cayley_field) (c: cayley_cell) =
  Hash.find f c


;;




let empty p = empty_field (), p

exception MapNext

let map fct (f,p) =
  let ret = empty_field () in
    Hash.iter (fun pos v -> try Hash.add ret pos (fct pos v) with MapNext -> ()) f;
    ret, p

let iter fct (f,_) =
  Hash.iter fct f
  
let iter_random fct (f,_) =
  Hash.iter_from_random_key fct f
  
let fold fct (f,_) zero =
  Hash.fold fct f zero

let forall fct (f,_) =
  Hash.forall fct f
  
let exists fct (f,_) =
  Hash.exists fct f

let size (f,_) =
  Hash.size f

let set (f,p) (c,p') d =
  if compare_graph p p' <> 0 then raise (Erreur "Core_gbf: setpos: incompatible Cayley graphs types")
  else
    let c =
      if (vector p c) then (
	to_point p (Array.copy c)
      ) else c
    in
      unsafe_set f c d

let get (f,p) (c,p') =
  if compare_graph p p' <> 0 then raise Not_found
  else
    let c =
      if (vector p c) then (
	to_point p (Array.copy c)
      ) else c
    in
      unsafe_get f c

let find g p = get g p

let nth n (f,_) =
  Hash.nth n f

let remove (f,p) (pos,p') =
  if compare_graph p p' = 0 then Hash.remove f pos

let copy (f,_) =
  Hash.copy f

let hd (f,_) =
  Hash.hd f

let last (f,_) =
  Hash.last f

let tl (f,_) =
  Hash.tl f

let mem (f,p) (pos,p') =
  if compare_graph p p' <> 0 then false
  else Hash.mem f pos

let compare valcmp (f1,p1) (f2,p2) =
  let d = compare_graph p1 p2 in
    if d <> 0 then d
    else Hash.compare valcmp f1 f2

let to_list (f,p) =
  fold (fun pos v s -> ((pos,p),v)::s) f []

let rec merge fct (f1,p) (f2,p') =
  if compare_graph p p' <> 0 then raise (Erreur "Core_gbf: merge: incompatible gbf")
  else
    let ret = Hash.copy f1 in
      merge_fields_in_place fct ret f2, p

and merge_fields_in_place fct f1 f2 =
  Hash.iter (fun p v2 -> try unsafe_set f1 p (fct (unsafe_get f1 p) v2) with Not_found -> unsafe_set f1 p v2) f2;
  f1

let following (pres: cayley_graph) (extract_array: 'a -> 'a array) (avoid_fct: 'a -> bool) (data: 'a) (dirs: cayley_cell list) =

  let f = empty_field () in

  let rec apply dt pos = function
    | [] -> raise (Erreur "Core_gbf: following: at least one direction is required")
    | [ dir ] -> (
	let p = ref pos in
	  Array.iter (fun d -> (if not(avoid_fct d) then unsafe_set f (!p) d); p := normalize pres (add (!p) dir)) dt
      )
    | dir :: t -> (
	let p = ref pos in
	  Array.iter (fun d -> apply (extract_array d) (!p) t; p := normalize pres (add (!p) dir)) dt
      )
  in

    apply (extract_array data) (origin pres) dirs;

    f
;;





let gbf_pos_from_gbf_expr _ = failwith "Core_gbf: gbf_pos_from_gbf_expr: Nyi"
;;
