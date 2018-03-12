// Import required java libraries
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import org.json.JSONObject;
import org.json.JSONArray;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

// Extend HttpServlet class
public class UpdateVoter extends HttpServlet {
 
   private String message;
   public static Connection connection = null;

   public void init() throws ServletException {
      // Do required initialization
      message = "Hello World";
   }

    public void UpdateDB(String Uname,String OldPasswd,String NewPasswd)throws SQLException{
	    JSONArray result = new JSONArray();
	    try{
	    String SelectSQL = "Update user set Upasswd = '"+NewPasswd+"' where Uname = '"+Uname+"' and Upasswd = '"+OldPasswd+"';";
	    Class.forName("org.sqlite.JDBC");
	    connection = DriverManager.getConnection("jdbc:sqlite:/tmp/vote.db");
	    Statement statement = null;
            statement = connection.createStatement();
            statement.executeUpdate(SelectSQL);
	    return;
	    }catch(Exception e){
		    e.printStackTrace();
		    return;
	    }
    }	

   public void doGet(HttpServletRequest request, HttpServletResponse response)
      throws ServletException, IOException {

      String Uname = request.getParameter("Uname");
      String OldPasswd = request.getParameter("OldPasswd");
      String NewPasswd = request.getParameter("NewPasswd");


	JSONObject result = new JSONObject();
	try{
		UpdateDB(Uname,OldPasswd,NewPasswd);
		result.put("result","0");
		result.write(response.getWriter());
	}catch(Exception e){}
      
   }

   public void destroy() {
      // do nothing.
   }
}
