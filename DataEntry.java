import java.time.LocalDateTime;

public class DataEntry {

    private String _status;
    private LocalDateTime _time;

    public DataEntry(String status, LocalDateTime time) {
        _status = status;
        _time = time;
    }

    public String getStatus() {
        return _status;
    }

    public LocalDateTime getTime() {
        return _time;
    }

    public String toString() {
        return getTime() + " - " + getStatus();
    }
}