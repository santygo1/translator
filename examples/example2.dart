decl empty(){}

myvar1 = 2;// this is first variable

decl condExample(var1){
    var2 = 2;
    print(var2);

    if(var1 > var2){
        print(var1);
        if(var2 == 3){
            print(var2);
        }
    }else{
        print(var2);
    }

    isVar = true;
    if(isVar){
        print(isVar);
    }

    if(true){
        print(true);
    }
}

decl loopExample(){
    var1 = "var1";
    while(true){
        print(var1);
    }

    var2 = "var2";
    while(var1 != var2){
        print(var2);
    }

    for(i = 0; (i + 1) < 10; i = i + 1){
        while(true){
            for(j = 0; j < 2; j = j + 2){ // one more comment
            }
        }
        print(var1); // this is print is embedded
    }
}

decl exampleLogic(){
    var1 = 10;
    var2 = var1;
    bool1 = (var1 + var2) > 10;
}

decl main(){
    condExample(10+1);
    var1 = 10;
    condExample(var1);

    loopExample();
}