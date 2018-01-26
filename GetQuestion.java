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
public class GetQuestion extends HttpServlet {
 
   private String message;
   public static Connection connection = null;

   public void init() throws ServletException {
      // Do required initialization
      message = "Hello World";
   }

    public JSONArray selectAll()throws SQLException{
	    JSONArray result = new JSONArray();
	    try{
	    String SelectSQL = "select * from question_list;";
	    Class.forName("org.sqlite.JDBC");
	    connection = DriverManager.getConnection("jdbc:sqlite:/tmp/answer_game.db");
	    Statement statement = null;
            ResultSet rs = null;
            statement = connection.createStatement();
            rs = statement.executeQuery(SelectSQL);
	    while(rs.next()){
		    JSONObject tmp = new JSONObject();
		    tmp.put("contract_address",rs.getString("contract_address"));
		    tmp.put("abi",rs.getString("abi"));
		    tmp.put("account",rs.getString("account"));
		    tmp.put("question",rs.getString("question"));
		    tmp.put("answer",rs.getString("answer"));
		    tmp.put("deadline",rs.getString("deadline"));
		    result.put(tmp);
	    }
	    return result;
	    }catch(Exception e){
		    e.printStackTrace();
		    return result;
	    }
    }	

	public static JSONObject contract_deploy(String host,String passwd, String contract_address, String behavior) throws IOException {
                ProcessBuilder pb = new ProcessBuilder();
                pb.redirectErrorStream(true);
                pb.command("python3", "/home/yenkuanlee/TEST/contract/e.py",host,passwd,contract_address,behavior);
                Process process = pb.start();
                java.io.InputStream inputStream = process.getInputStream();
                BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
                String line = null;
		JSONObject result = new JSONObject();
                while ((line = reader.readLine()) != null) {
			try{
				result.put("output",line);
			}catch(Exception e){}
                }
		return result;
        }

   public void doGet(HttpServletRequest request, HttpServletResponse response)
      throws ServletException, IOException {
	//JSONObject joParam = request.getParameter(request);
	//String host = joParam.optString("host");
	//String account = joParam.optString("account");
	//String passwd = joParam.optString("passwd");
	//String host = request.getParameter("host");
	//String passwd = request.getParameter("passwd");
	//String behavior = request.getParameter("behavior");
	//String contract_address = request.getParameter("contract_address");
	//String question = request.getParameter("question");
	

	JSONObject result = new JSONObject();
	//result = contract_deploy(host,passwd,contract_address,behavior);
	try{
		result.put("question_list",selectAll());
		result.put("result","0");
		//result.put("answer",answer);
		//result.put("deadline",duration);
		result.write(response.getWriter());
	}catch(Exception e){}
      
      // Set response content type
      ///response.setContentType("text/html");

      // Actual logic goes here.
      ///PrintWriter out = response.getWriter();
      ///out.println("<h1>" + message + "</h1>");
   }

   public void destroy() {
      // do nothing.
   }
}
