import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.time.LocalDateTime;

public enum Service {
    BITBUCKET("https://status.bitbucket.org", "<span class=\"status.*?>.*?</span>", "All Systems Operational"),
    SLACK("https://status.slack.com", "<div id=\"current_status\".*?</div>", "Slack is up and running");

    private String _url, _regex, _online;
    private List<DataEntry> _entries = new ArrayList<>();

    Service(String url, String regex, String on) {
        _url = url;
        _regex = regex;
        _online = on;
    }

    public DataEntry isOnline() {
        // connects to url of each service
        URL connection;
        try {
            connection = new URL(_url);
        } catch (MalformedURLException e) {
            DataEntry d = new DataEntry("down", LocalDateTime.now());
            _entries.add(d);
            return d;
        }

        // get all html from webpage
        BufferedReader in = null;
        StringBuilder data = new StringBuilder();
        try {
            in = new BufferedReader(new InputStreamReader(connection.openStream()));
            String input;
            while ((input = in.readLine()) != null)
                data.append(input);
            in.close();
        } catch (IOException | NullPointerException e) {
            DataEntry d = new DataEntry("down", LocalDateTime.now());
            _entries.add(d);
            return d;
        }

        // Validate if service is online by matching patterns
        Pattern exp = Pattern.compile(_regex);
        Matcher matcher = exp.matcher(data.toString());
        DataEntry entry = new DataEntry((matcher.find() && matcher.group().contains(_online) ? "up" : "down"),
                LocalDateTime.now());
        _entries.add(entry);
        return entry;

    }

    public String toString() {
        return this.name().toLowerCase();
    }

    public void load(List<DataEntry> data) {
        _entries = data;
    }

    public List<String> getHistory() {
        List<String> ret = new ArrayList<>();
        for (int i = _entries.size() - 1; i >= 0; i--) {
            ret.add(_entries.get(i).toString());
        }
        
        return ret;
    }
 
}