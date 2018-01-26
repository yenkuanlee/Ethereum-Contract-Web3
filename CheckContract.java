// Import required java libraries
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import org.json.JSONObject;



// Extend HttpServlet class
public class CheckContract extends HttpServlet {
 
   private String message;

   public void init() throws ServletException {
      // Do required initialization
      message = "Hello World";
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
	String host = request.getParameter("host");
	String passwd = request.getParameter("passwd");
	String behavior = request.getParameter("behavior");
	String contract_address = request.getParameter("contract_address");
	//String question = request.getParameter("question");
	

	JSONObject result = new JSONObject();
	result = contract_deploy(host,passwd,contract_address,behavior);
	try{
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
