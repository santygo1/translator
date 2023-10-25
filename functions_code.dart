decl function(var1){
    var2 = var1;
    var2 = 10 + var2;
}

decl main(var1){
    var1 = true;
    var2 = left && (1 > 2);
    print(var1 || var2);

    var3 = 1;
    var4 = 2;
    print(var3 + var4);
    print((var3 * 2 + (var4 * 3) - 1 * 10) > 10);

    if(var3 > var1){
        print("if");
    };

    for(var2 = 0; var2 < 10; var2 = var2 + 1){
        print("for");
    };

    doubleVar = 2.0;
    print(doubleVar);

    str = "This is string";
    print(str);
}