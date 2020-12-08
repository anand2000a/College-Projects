/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package audi_indore;
import java.sql.*;
import javax.swing.*;

/**
 *
 * @author Ankit Gehlot
 */
public class connector {
    Connection conn = null;
    public static Connection ConnectDB(){
        try{
            Class.forName("com.mysql.jdbc.Driver");
            Connection conn =  DriverManager.getConnection("jdbc:mysql://localhost/sales_n_services","root","anuj");
            JOptionPane.showMessageDialog(null,"connection establised");
            return conn;
        }
        catch(Exception e){
            JOptionPane.showMessageDialog(null,e);
            return null;
        }
    }
    
}
