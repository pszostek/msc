#!/usr/bin/env bash
JLIBSVM_HOME=/home/$(whoami)/msc/jlibsvm
alias svm_train="java -cp $JLIBSVM_HOME/target/jlibsvm-0.92-SNAPSHOT.jar edu.berkeley.compbio.jlibsvm.legacyexec.svm_train"
alias svm_scale="java -cp $JLIBSVM_HOME/target/jlibsvm-0.92-SNAPSHOT.jar edu.berkeley.compbio.jlibsvm.legacyexec.svm_train"
alias svm_predict="java -cp $JLIBSVM_HOME/target/jlibsvm-0.92-SNAPSHOT.jar edu.berkeley.compbio.jlibsvm.legacyexec.svm_train"
alias svm_toy="java -cp $JLIBSVM_HOME/target/jlibsvm-0.92-SNAPSHOT.jar edu.berkeley.compbio.jlibsvm.legacyexec.svm_train"
