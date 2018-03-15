// Import required java libraries
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import org.json.JSONObject;

// Extend HttpServlet class
public class GetAppInfo extends HttpServlet {
 
   private String message;

   public void init() throws ServletException {
      // Do required initialization
      message = "Hello World";
   }
	public static JSONObject contract_deploy(String app) throws IOException {
                ProcessBuilder pb = new ProcessBuilder();
                pb.redirectErrorStream(true);
                pb.command("python3", "/home/localadmin/Ethereum-Contract-Web3/Application/GetAppInfo.py",app);
                Process process = pb.start();
                java.io.InputStream inputStream = process.getInputStream();
                BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
                String line = null;
		JSONObject result = new JSONObject();
		line = reader.readLine();
                while ((line = reader.readLine()) != null) {
			try{
        		        result.put("output",line);
	                }catch(Exception e){ line = e.getMessage();}
                }
		try{
			result.put("app",app);
		}catch(Exception e){}
		return result;
        }

   public void doGet(HttpServletRequest request, HttpServletResponse response)
      throws ServletException, IOException {
	String app = request.getParameter("app");
	

	JSONObject result = new JSONObject();
	result = contract_deploy(app);
	try{
		result.put("result","0");
		result.write(response.getWriter());
	}catch(Exception e){}

   }

   public void destroy() {
      // do nothing.
   }
}
