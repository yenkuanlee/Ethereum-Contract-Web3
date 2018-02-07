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
public class GetVote extends HttpServlet {
 
   private String message;
   public static Connection connection = null;

   public void init() throws ServletException {
      // Do required initialization
      message = "Hello World";
   }

    public JSONArray selectAll()throws SQLException{
	    JSONArray result = new JSONArray();
	    try{
	    String SelectSQL = "select * from Vote;";
	    Class.forName("org.sqlite.JDBC");
	    connection = DriverManager.getConnection("jdbc:sqlite:/tmp/vote.db");
	    Statement statement = null;
            ResultSet rs = null;
            statement = connection.createStatement();
            rs = statement.executeQuery(SelectSQL);
	    while(rs.next()){
		    JSONObject tmp = new JSONObject();
		    tmp.put("contract_address",rs.getString("contract_address"));
		    tmp.put("account",rs.getString("account"));
		    tmp.put("topic",rs.getString("topic"));
		    tmp.put("_numProposals",rs.getString("_numProposals"));
		    tmp.put("prop",rs.getString("prop"));
		    result.put(tmp);
	    }
	    return result;
	    }catch(Exception e){
		    e.printStackTrace();
		    return result;
	    }
    }	



   public void doGet(HttpServletRequest request, HttpServletResponse response)
      throws ServletException, IOException {

	JSONObject result = new JSONObject();
	try{
		result.put("vote_list",selectAll());
		result.put("result","0");
		result.write(response.getWriter());
	}catch(Exception e){}
      
   }

   public void destroy() {
      // do nothing.
   }
}
