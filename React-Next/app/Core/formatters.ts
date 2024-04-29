export function formatDate(d: Date | string | number) {
  const date = new Date(d);
  const year = date.getFullYear();
  const month = ("0" + (date.getMonth() + 1)).slice(-2);
  const day = ("0" + date.getDate()).slice(-2);
  const hours = ("0" + date.getHours()).slice(-2);
  const minutes = ("0" + date.getMinutes()).slice(-2);
  const formattedDateTime = `${month}/${day}/${year}`;
  return formattedDateTime;
}
