// Import required java libraries
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import org.json.JSONObject;

// Extend HttpServlet class
public class Vote extends HttpServlet {
 
   private String message;

   public void init() throws ServletException {
      // Do required initialization
      message = "Hello World";
   }
	public static JSONObject vote(String host,String account,String passwd, String contract_address, String to_Voter, String cnt) throws IOException {
                ProcessBuilder pb = new ProcessBuilder();
                pb.redirectErrorStream(true);
                pb.command("python3", "/home/yenkuanlee/TEST/Ethereum-Contract-Web3/VoteEX/Vote.py",host,account,passwd,contract_address,to_Voter,cnt);
                Process process = pb.start();
                java.io.InputStream inputStream = process.getInputStream();
                BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
                String line = null;
		JSONObject result = new JSONObject();
		try{
			result.put("host",host);
			result.put("account",account);
			result.put("passwd",passwd);
			result.put("contract_address",contract_address);
			result.put("to_Voter",to_Voter);
			result.put("cnt",cnt);
		}catch(Exception e){}
		return result;
        }

   public void doGet(HttpServletRequest request, HttpServletResponse response)
      throws ServletException, IOException {
	String host = request.getParameter("host");
	String account = request.getParameter("account");
	String passwd = request.getParameter("passwd");
	String to_Voter= request.getParameter("to_Voter");
	String cnt = request.getParameter("cnt");
	String contract_address = request.getParameter("contract_address");
	

	JSONObject result = new JSONObject();
	result = vote(host,account,passwd,contract_address,to_Voter,cnt);
	try{
		result.put("result","0");
		result.write(response.getWriter());
	}catch(Exception e){}
   }

   public void destroy() {
      // do nothing.
   }
}
