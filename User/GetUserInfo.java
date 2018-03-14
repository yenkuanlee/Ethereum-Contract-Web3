// Import required java libraries
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import org.json.JSONObject;

// Extend HttpServlet class
public class GetUserInfo extends HttpServlet {
 
   private String message;

   public void init() throws ServletException {
      // Do required initialization
      message = "Hello World";
   }
	public static JSONObject contract_deploy(String Uname, String Upasswd) throws IOException {
                ProcessBuilder pb = new ProcessBuilder();
                pb.redirectErrorStream(true);
                pb.command("python3", "/home/localadmin/Ethereum-Contract-Web3/VoteEX/GetInfo.py",Uname,Upasswd);
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
	String Uname = request.getParameter("Uname");
	String Upasswd = request.getParameter("Upasswd");
	

	JSONObject result = new JSONObject();
	result = contract_deploy(Uname,Upasswd);
	try{
		result.put("result","0");
		result.write(response.getWriter());
	}catch(Exception e){}

   }

   public void destroy() {
      // do nothing.
   }
}
