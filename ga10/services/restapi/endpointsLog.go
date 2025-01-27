package restapi

import(
	"log"
	"reflect"

	"net/http"
	"strconv"

	"a10/operations"
	"a10/structures"
)

import(
	"github.com/labstack/echo/v4"
)

type returnLogEntries struct {
	LogEntries  []structures.LogEntry  `json:"logentries"`
	Length    int                      `json:"length"`
	Max	      int64                    `json:"max"`
}


func getLogEntries(c echo.Context) error {
	max_query := c.QueryParam("max")
	max, err := strconv.ParseInt(max_query, 10, 64)
	if err != nil {
		max=200
	}
	log.Println("maxtype is ",reflect.TypeOf(max))

	logentries,err := operations.GetLogEntries(max)

	if err != nil {
		return c.String(http.StatusInternalServerError,"error")
	} else {
		rtn := returnLogEntries{ logentries, len(logentries), max }
		return c.JSON(http.StatusOK, rtn)
	}
}
