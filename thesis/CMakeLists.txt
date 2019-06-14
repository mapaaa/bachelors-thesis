cmake_minimum_required(VERSION 2.8.4)

project(Thesis NONE)

include(UseLATEX.cmake)

set(Images
  UNIBUClogo.eps
  )

add_latex_document(
  thesis.tex
  INPUTS abstract.tex appendix.tex conclusion.tex experiment.tex extrapackages.tex layoutsetup.tex macrosetup.tex rankdistance.tex rules.tex theoremsetup.tex thesisintro.tex wordproduction.tex
  BIBFILES refs.bib
  IMAGES ${Images}
  )
