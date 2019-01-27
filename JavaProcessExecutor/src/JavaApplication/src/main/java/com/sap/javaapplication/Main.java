package com.sap.javaapplication;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main
{
    public static void main( String[] args )
    {
        InputStreamReader inputStreamReader = new InputStreamReader(System.in);
        BufferedReader bufferedReader = new BufferedReader(inputStreamReader);

        String line = null;
                       
        try {
            
            while ((line = bufferedReader.readLine()) != null ) {
                                
                if ( args.length == 0 ) {
                    System.err.println( "No Mode specified." );
                    continue;
                } 
                if ( line.length() == 0 ) { 
                    System.err.println( "Received empty value." );
                    continue;
                } 
                
                if ( args[0].toUpperCase().equals( "LENGTH" ) ) {
                    System.out.println( "String \"" + line + "\" has length " + line.length() );
                } else if ( args[0].toUpperCase().equals( "UPPER" ) ) {
                    System.out.println( line + " -> " + line.toUpperCase() );                
                } else {
                    System.err.println( "Mode " + args[0] + " is unknown.." );                            
                }
            }
    
        } catch (IOException e) {
            System.err.println(e.toString());
        }
    }
}
