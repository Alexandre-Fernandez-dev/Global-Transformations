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
 * File: $RCSfile: def_gbf.ml,v $
 * Symbolic name : $Name:  $
 * Author: OM, JLG
 * Modified: $Date: 2014-06-19 22:08:42 $
 * Version: $Revision: 1.6 $
 * -------------------------------------------------------------------
 *
 * Status:  
 *     La representation d'un GBF.
 *
 *=========================================================================
 *)


open Global
open Number
open Linear

type 'a smith_spec = {
  m: 'a matrix; (* Matrix *)
  a: 'a matrix; (* Diagonalized Matrix *)
  l: 'a matrix; (* Left Matrix s.t. A = L M R *)
  r: 'a matrix; (* Right Matrix s.t. A = L M R *)
  l_inv: 'a matrix; (* Inverse of L *)
  r_inv: 'a matrix; (* Inverse of R *)
}

and cayley_graph = {

  (* Unique identifier for quick comparison *)
  id: int;

  (* Smith decomposition: for memory only *)
  smith_spec: num smith_spec;

  (* Group specification (normalized group) *)
  rank:     int;               (* dimension of the coordinate system *)
  torsions: int vector;        (* not null torsion coefficients      *)
  order:    int;               (* group order (0 for infinity)       *)
  of_graph: int matrix;        (* L matrix                           *)
  basis:    int vector array;  (* copy of L in an array of columns   *)
  neighbors: int vector array; (* array of neighbors *)

  (* Graph specification (original group) *)
  degree:   int;        (* number of out-going arrows (in fact half degree) *)
  orders:   int vector; (* number of steps for cycling (0 for infinity)     *)
  to_graph: int matrix; (* L^-1 matrix                                      *)

}

and cayley_cell = int vector

and 'a cayley_field = (cayley_cell, 'a) Hash.t

and 'a tgbf = 'a cayley_field * cayley_graph

and posgbf = cayley_cell * cayley_graph

and posgbf_type =
  | GbfVector
  | GbfPoint
;;








