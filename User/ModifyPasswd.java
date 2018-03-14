// Import required java libraries
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import org.json.JSONObject;

// Extend HttpServlet class
public class ModifyPasswd extends HttpServlet {
 
   private String message;

   public void init() throws ServletException {
      // Do required initialization
      message = "Hello World";
   }
	public static JSONObject vote(String Uname, String op, String np) throws IOException {
                ProcessBuilder pb = new ProcessBuilder();
                pb.redirectErrorStream(true);
                pb.command("python3", "/home/localadmin/Ethereum-Contract-Web3/User/ModifyPasswd.py",Uname,op,np);
                Process process = pb.start();
                java.io.InputStream inputStream = process.getInputStream();
                BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
                String line = null;
		JSONObject result = new JSONObject();
		try{
		}catch(Exception e){}
		return result;
        }

   public void doGet(HttpServletRequest request, HttpServletResponse response)
      throws ServletException, IOException {
	String Uname = request.getParameter("Uname");
	String op = request.getParameter("op");
	String np = request.getParameter("np");
	

	JSONObject result = new JSONObject();
	result = vote(Uname,op,np);
	try{
		result.put("result","0");
		result.write(response.getWriter());
	}catch(Exception e){}
   }

   public void destroy() {
      // do nothing.
   }
}
